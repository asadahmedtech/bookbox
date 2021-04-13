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
                
                for seatID in request.data['seats']:
                    showSeat = ShowSeat.objects.get(id=seatID)
                    if(showSeat.status == False):
                        showSeat.status = True
                        showSeat.booking = booking
                        showSeat.save()
                    else:
                        return Response('Seat already booked', status=status.HTTP_422_UNPROCESSABLE_ENTITY)

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


