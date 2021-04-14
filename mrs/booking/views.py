from django.shortcuts import render
from django.db import transaction
from django.db.models import Sum
from datetime import datetime, timedelta

from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from booking.models import *
from booking.serializers import *
from booking.task import *

booking_param = openapi.Parameter('bookingID', openapi.IN_QUERY, description="ID of the booking made", type=openapi.TYPE_INTEGER)
user_param = openapi.Parameter('user', openapi.IN_BODY, description="name of the user", type=openapi.TYPE_STRING)
show_param = openapi.Parameter('showID', openapi.IN_BODY, description="ID of the show", type=openapi.TYPE_INTEGER)
seat_param = openapi.Parameter('seats', openapi.IN_BODY, description="Array of seat IDs for a given show", type=openapi.TYPE_ARRAY, items=openapi.TYPE_STRING)
payment_param = openapi.Parameter('paymentID', openapi.IN_QUERY, description="ID of the payment made", type=openapi.TYPE_INTEGER)
payment_body_param = openapi.Parameter('paymentID', openapi.IN_BODY, description="ID of the payment made", type=openapi.TYPE_INTEGER)
status_param = openapi.Parameter('status', openapi.IN_BODY, description="status of transaction", type=openapi.TYPE_STRING)
transaction_param = openapi.Parameter('transactionID', openapi.IN_BODY, description="ID of transaction", type=openapi.TYPE_STRING)

# Create your views here.
class BookingList(APIView):
    '''
    description: This API Lists and Creates Bookings for users. 
    '''

    @swagger_auto_schema(manual_parameters=[booking_param],)
    def get(self, request, format=None):
        '''
        description: This API Lists all booking informations. 
                    The list can be filtered using optional query paramaters like bookingID
        parameters:
        - name: bookingID
            description: booking ID
            type: string
            required: false
            location: query
        '''

        booking = self.get_queryset()
        serializer = BookingSerializer(booking, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=openapi.Schema(
                             type=openapi.TYPE_OBJECT,
                             required=['version'],
                             properties={
                                 'show': show_param,
                                 'user': user_param,
                                 'seats': seat_param,
                             },
                         ),
                         operation_description='Add a Booking in a show')
    def post(self, request, format=None):
        '''
        description: This API Creates Booking for users.
        parameters:
        - name: showID
            description: ID of the show
            type: string 
            required: true
            location: body
        - name: user
            description: name of user
            type: string
            required: true
            location: body
        - name: seats
            description: list of seat IDs available in the given show
            type: array string
            required: true
            location: body
        '''

        try:
            if(request.data['showID'] and request.data['user']):
                show = Show.objects.get(id=request.data['showID'])

                # Verify and block the seats if they are empty
                if not self.verify_seats(request.data['seats']):
                    return Response('Seat already booked', status=status.HTTP_422_UNPROCESSABLE_ENTITY)

                created_at = datetime.now()
                booking = Booking.objects.create(created_at=created_at, show=show, user=request.data['user'], status='PROG')
                
                amount = 0
                with transaction.atomic():
                    ShowSeat.objects.filter(id__in=request.data['seats']).update(booking=booking)
                    amount = ShowSeat.objects.filter(id__in=request.data['seats']).aggregate(amount=Sum('price'))['amount']

                #Create Payment Object this will be calling payment gateways
                payment = Payment.objects.create(booking=booking, created_at=created_at, amount=amount)

                serializer = BookingSerializer(booking)

                #Apply async unreserve hook
                three_mins_hence = datetime.utcnow() + timedelta(minutes=15)
                unbook_seat_task.apply_async((booking.id,), eta=three_mins_hence)

                return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            #In case of payment failures or domain failures, seats will be unreserved 
            print(str(e))
            self.unreserve_seats(request.data['seats'])
            return Response('', status=status.HTTP_400_BAD_REQUEST)
        
    # Filters the queryset based on optional parameters provided
    def get_queryset(self):
        queryset = Booking.objects.all()
        bookingID = self.request.query_params.get('bookingID')

        # Filter theater based on booking id
        if bookingID:
            queryset = queryset.filter(id=bookingID)
        
        return queryset
    
    #Verify the seats selected as empty
    def verify_seats(self, seatsList):
        # return self.unreserve_seats(seatsList)

        for seatID in seatsList:
            showSeat = ShowSeat.objects.get(id=seatID)
            if(showSeat.status == True):
                return False
        
        with transaction.atomic():
            ShowSeat.objects.filter(id__in=seatsList).update(status=True)

        return True

    #Unreserve the blocked seats if somethings crashes
    def unreserve_seats(self, seatsList):
        ShowSeat.objects.filter(id__in=seatsList).update(status=False)
        return False

class ShowSeatList(generics.ListCreateAPIView):
    '''
    description: This API Lists and Creates Seating information for a give show.
    parameters:
    - name: seat
        description: ID of the seat in a given theater
        type: int
        required: true
        location: body
    - name: price
        description: cost of given seat in a showtime
        type: float
        required: true
        location: body
    - name: show
        description: ID of the show in a given theater
        type: int
        required: true
        location: body
    '''
    model = ShowSeat
    serializer_class = ShowSeatSerializer

    # Filters the queryset based on optional parameters provided
    def get_queryset(self):
        queryset = ShowSeat.objects.all()
        showID = self.request.query_params.get('showID')

        # Filter theater based on show id
        if showID:
            queryset = queryset.filter(show__id=showID)
        
        return queryset

class PaymentList(APIView):
    '''
    description: This API Lists and Creates Payment transactions with gateways for users. 
    '''

    @swagger_auto_schema(manual_parameters=[payment_param],)
    def get(self, request, format=None):
        '''
        description: This API Lists all payment informations. 
                    The list can be filtered using optional query paramaters like paymentID
        parameters:
        - name: paymentID
            description: payment ID
            type: string
            required: false
            location: query
        '''
        payment = self.get_queryset()
        serializer = PaymentSerializer(payment, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=openapi.Schema(
                             type=openapi.TYPE_OBJECT,
                             required=['version'],
                             properties={
                                 'paymentID': payment_param,
                                 'status': status_param,
                                 'transactionID': transaction_param,
                             },
                         ),
                         operation_description='Update a payment')
    def post(self, request, format=None):
        '''
        description: This API updates payment for users. In case of payment failures the seats get unreserved
        parameters:
        - name: paymentID
            description: ID of the payment
            type: string 
            required: true
            location: body
        - name: status
            description: status from transaction made Success/Failed
            type: string
            required: true
            location: body
        - name: transactionID
            description: ID of the transaction made
            type: string
            required: true
            location: body
        '''
        try:
            if(request.data['paymentID'] and request.data['status']):
                payment = Payment.objects.get(id=request.data['paymentID'])
                booking = Booking.objects.get(id=payment.booking.id)
                print(request.data)
                if booking.status == 'FAIL':
                    #Spawn a payment refund process
                    return Response('Booking Timeout', status=status.HTTP_422_UNPROCESSABLE_ENTITY)
                if request.data['status'] == "Success":
                    payment.transactionID = request.data['transactionID']
                    booking.status = 'SUCC'
                else:
                    booking.status = 'FAIL'
                    ShowSeat.objects.filter(booking=booking.id).update(status=False)
                    ShowSeat.objects.filter(booking=booking.id).update(booking=None)
                
                booking.save()
                payment.save()
                
                serializer = PaymentSerializer(payment)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        except KeyError:
            return Response('', status=status.HTTP_400_BAD_REQUEST)

    # Filters the queryset based on optional parameters provided
    def get_queryset(self):
        queryset = Payment.objects.all()
        paymentID = self.request.query_params.get('paymentID')

        # Filter theater based on payment id
        if paymentID:
            queryset = queryset.filter(id=paymentID)
        
        return queryset

