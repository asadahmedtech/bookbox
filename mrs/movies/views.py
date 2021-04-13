from django.shortcuts import render
from movies.models import *
from movies.serializers import *
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

test_param = openapi.Parameter('test', openapi.IN_QUERY, description="test manual param", type=openapi.TYPE_BOOLEAN)

# Create your views here.
class CityList(generics.ListCreateAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer

class TheaterList(APIView):
    '''
    description: This API deletes/uninstalls a device.
    parameters:
    - name: name
        type: string
        required: true
        location: form
    - name: bloodgroup
        type: string
        required: true
        location: form
    - name: birthmark
        type: string
        required: true
        location: form
    '''
    # serializer_class = TheaterSerializer
    @swagger_auto_schema(manual_parameters=[test_param],)
    def get(self, request, format=None):
        theater = self.get_queryset()
        serializer = TheaterSerializer(theater, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        print(request.data)
        try:
            if(request.data['name'] and request.data['city'] and request.data['address']):
                city = City.objects.get(city=request.data['city'])
                theater = Theater.objects.create(city=city, name=request.data['name'], address=request.data['address'])
                serializer = TheaterSerializer(theater)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response('Inavlid parameters', status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        queryset = Theater.objects.all()
        cityID = self.request.query_params.get('city')
        movieID = self.request.query_params.get('movie')

        if cityID:
            queryset = queryset.filter(city__city=cityID)
        if movieID:
            showqueryset = Show.objects.all()
            showqueryset = showqueryset.filter(movie__name=movieID).values_list('theater__id', flat=True)
            queryset = queryset.filter(id__in=showqueryset)
        
        return queryset

class TheaterSeatList(APIView):
    def get(self, request, format=None):
        theaterseat = TheaterSeat.objects.all()
        serializer = TheaterSeatSerializer(theaterseat, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        print(request.data)
        try:
            if(request.data['seatNumber'] and request.data['seatType'] and request.data['theater']):
                theater = Theater.objects.get(id=request.data['theater'])
                theaterseat = TheaterSeat.objects.create(seatNumber=request.data['seatNumber'], theater=theater, seatType=request.data['seatType'])
                serializer = TheaterSeatSerializer(theaterseat)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response('Inavlid parameters', status=status.HTTP_400_BAD_REQUEST)

class MovieList(generics.ListCreateAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

class ShowList(APIView):
    def get(self, request, format=None):
        show = self.get_queryset()
        serializer = ShowSerializer(show, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        print(request.data)
        try:
            if(request.data['movie'] and request.data['theater'] and request.data['showtime']):
                movie = Movie.objects.get(name=request.data['movie'])
                theater = Theater.objects.get(name=request.data['theater'])
                show = Show.objects.create(movie=movie, theater=theater, show_time=request.data['showtime'])
                serializer = ShowSerializer(show)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response('Inavlid parameters', status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        queryset = Show.objects.all()
        cityID = self.request.query_params.get('city')
        theaterID = self.request.query_params.get('theater')
        movieID = self.request.query_params.get('movie')

        if movieID:
            queryset = queryset.filter(movie__name=movieID)
        if theaterID:
            queryset = queryset.filter(theater=theaterID)
        if cityID:
            queryset = queryset.filter(theater__city__city=cityID)
        
        return queryset

