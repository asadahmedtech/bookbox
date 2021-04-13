from django.shortcuts import render
from booking.models import *
from booking.serializers import *
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# Create your views here.
class BookingList(APIView):
    def get(self, request, format=None):
        booking = Booking.objects.all()
        serializer = BookingSerializer(booking, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        print(request.data)
        try:
            if(request.data['showID'] and request.data['user']):
                show = Show.objects.get(id=request.data['showID'])
                created_at = datetime.now()
                booking = Booking.objects.create(created_at=created_at, show=show, user=request.data['user'])
                
                amount = 0

                for seatID in request.data['seats']:
                    showSeat = ShowSeat.objects.get(id=seatID)
                    if(showSeat.status == False):
                        showSeat.status = True
                        showSeat.booking = booking
                        amount += showSeat.price
                        showSeat.save()
                    else:
                        return Response('Seat already booked', status=status.HTTP_422_UNPROCESSABLE_ENTITY)

                #Create Payment Object
                payment = Payment.objects.create(booking=booking, created_at=created_at, amount=amount)
                ##Block Seats
                serializer = BookingSerializer(booking)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        except KeyError:
            return Response('', status=status.HTTP_400_BAD_REQUEST)
        # serializer = BookingSerializer(data=request.data)
        # if serializer.is_valid():
        #     serializer.save()
        #     return Response(serializer.data, status=status.HTTP_201_CREATED)
        


class ShowSeatList(generics.ListCreateAPIView):
    queryset = ShowSeat.objects.all()
    serializer_class = ShowSeatSerializer

# class PaymentList(generics.ListCreateAPIView):
#     queryset = Payment.objects.all()
#     serializer_class = PaymentSerializer

class PaymentList(APIView):
    def get(self, request, format=None):
        payment = Payment.objects.all()
        serializer = PaymentSerializer(payment, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        print(request.data)
        try:
            if(request.data['paymentID'] and request.data['status']):
                payment = Payment.objects.get(id=request.data['paymentID'])
                booking = Booking.objects.get(id=payment.booking.id)
                if request.data['status'] == "Success":
                    payment.transactionID = request.data['transactionID']
                    booking.status = True
                else:
                    booking.status = False
                    ShowSeat.objects.filter(booking=booking.id).update(status=False)
                    ShowSeat.objects.filter(booking=booking.id).update(booking=None)
                
                booking.save()
                payment.save()
                
                serializer = PaymentSerializer(payment)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        except KeyError:
            return Response('', status=status.HTTP_400_BAD_REQUEST)


