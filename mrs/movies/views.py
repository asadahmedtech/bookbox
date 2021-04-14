from django.shortcuts import render

from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from movies.models import *
from movies.serializers import *

city_param = openapi.Parameter('cityID', openapi.IN_QUERY, description="Name of the city", type=openapi.TYPE_STRING)
movie_param = openapi.Parameter('movieID', openapi.IN_QUERY, description="Name of the movie", type=openapi.TYPE_STRING)
show_param = openapi.Parameter('showID', openapi.IN_QUERY, description="ID of the show", type=openapi.TYPE_INTEGER)
theater_param = openapi.Parameter('theater', openapi.IN_QUERY, description="ID of the theater", type=openapi.TYPE_INTEGER)
theaterid_body_param = openapi.Parameter('theaterID', openapi.IN_BODY, description="ID of the theater", type=openapi.TYPE_INTEGER)
theater_body_param = openapi.Parameter('theater_name', openapi.IN_BODY, description="Name of the theater", type=openapi.TYPE_INTEGER)
city_body_param = openapi.Parameter('city', openapi.IN_BODY, description="Name of the city", type=openapi.TYPE_STRING)
address_param = openapi.Parameter('address', openapi.IN_BODY, description="ID of the theater", type=openapi.TYPE_INTEGER)
seattype_body_param = openapi.Parameter('seatType', openapi.IN_BODY, description="Type of the seat", type=openapi.TYPE_STRING)
seatnumber_body_param = openapi.Parameter('seatNumber', openapi.IN_BODY, description="Number of the seat", type=openapi.TYPE_STRING)
movie_body_param = openapi.Parameter('movie', openapi.IN_BODY, description="Name of the movie", type=openapi.TYPE_STRING)
showtime_body_param = openapi.Parameter('showtime', openapi.IN_BODY, description="Date and Time of the show", type=openapi.TYPE_STRING)

# Create your views here.
class CityList(generics.ListCreateAPIView):
    '''
    description: This API Lists and Creates City informations.
    parameters:
    - name: city
        type: string enum
        required: true
        location: body
    - name: state
        type: string
        required: true
        location: body
    - name: zipcode
        type: int
        required: true
        location: body
    '''

    queryset = City.objects.all()
    serializer_class = CitySerializer

class TheaterList(APIView):
    '''
    description: This API Lists and Creates Theater informations. 
                 The list can be filtered using optional query paramaters like city name and movie name
    '''

    @swagger_auto_schema(manual_parameters=[city_param, movie_param],)
    def get(self, request, format=None):
        '''
        description: This API Lists and Creates Theater informations. 
                    The list can be filtered using optional query paramaters like city name and movie name
        parameters:
        - name: city
            description: name of the city
            type: string enum
            required: true
            location: query
        - name: movie
            description: name of the movie
            type: string
            required: true
            location: query
        '''

        theater = self.get_queryset()
        serializer = TheaterSerializer(theater, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=openapi.Schema(
                             type=openapi.TYPE_OBJECT,
                             required=['version'],
                             properties={
                                 'theater': theater_body_param,
                                 'city': city_body_param,
                                 'address': address_param,
                             },
                         ),
                         operation_description='Add a theater')
    def post(self, request, format=None):
        '''
        description: This API Creates Theater informations.
        parameters:
        - name: name
            description: name of the theater
            type: string 
            required: true
            location: body
        - name: city
            description: name of the city
            type: string
            required: true
            location: body
        - name: address
            description: address of the theater
            type: string
            required: true
            location: body
        '''

        try:
            if(request.data['name'] and request.data['city'] and request.data['address']):
                try:
                    city = City.objects.get(city=request.data['city'])
                except City.DoesNotExist:
                    return Response('City Not Found', status=status.HTTP_404_NOT_FOUND)

                theater = Theater.objects.create(city=city, name=request.data['name'], address=request.data['address'])
                serializer = TheaterSerializer(theater)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response('Inavlid parameters', status=status.HTTP_400_BAD_REQUEST)

    # Filters the queryset based on optional parameters provided
    def get_queryset(self):
        queryset = Theater.objects.all()
        cityID = self.request.query_params.get('city')
        movieID = self.request.query_params.get('movie')

        # Filter theater based on city name
        if cityID:
            queryset = queryset.filter(city__city=cityID)
        # Filter theater based on movie name
        if movieID:

            #Finds the reverse FK mapping from shows and lists the theaters down.
            showqueryset = Show.objects.all()
            showqueryset = showqueryset.filter(movie__name=movieID).values_list('theater__id', flat=True)
            queryset = queryset.filter(id__in=showqueryset)
        
        return queryset

class TheaterSeatList(APIView):
    '''
    description: This API Lists and Creates Theater Seating informations of a particular theater. 
                The list can be filtered using optional query paramaters theaterID

    '''
    @swagger_auto_schema(manual_parameters=[theater_param],)
    def get(self, request, format=None):
        '''
        description: This API Lists Theater Seating informations. 
        parameters:
        - name: theater
            description: name of the theater
            type: string 
            required: true
            location: query
        '''
        theaterseat = self.get_queryset()
        serializer = TheaterSeatSerializer(theaterseat, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=openapi.Schema(
                             type=openapi.TYPE_OBJECT,
                             required=['version'],
                             properties={
                                 'theater': theaterid_body_param,
                                 'seatNumber': seatnumber_body_param,
                                 'seatType': seattype_body_param,
                             },
                         ),
                         operation_description='Add a Seat in Theater')
    def post(self, request, format=None):
        '''
        description: This API Creates Theater Seating informations.
        parameters:
        - name: theater
            description: ID of the theater
            type: string 
            required: true
            location: body
        - name: seatNumber
            description: seat number of the theater seat
            type: string
            required: true
            location: body
        - name: seatType
            description: type of the seat from premium/gold/front 
            type: string enum
            required: true
            location: body
        '''
        try:
            if(request.data['seatNumber'] and request.data['seatType'] and request.data['theater']):
                try:
                    theater = Theater.objects.get(id=request.data['theater'])
                except Theater.DoesNotExist:
                    return Response('Theater Not Found', status=status.HTTP_404_NOT_FOUND)

                theaterseat = TheaterSeat.objects.create(seatNumber=request.data['seatNumber'], theater=theater, seatType=request.data['seatType'])
                serializer = TheaterSeatSerializer(theaterseat)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response('Inavlid parameters', status=status.HTTP_400_BAD_REQUEST)
    
    # Filters the queryset based on optional parameters provided
    def get_queryset(self):
        queryset = TheaterSeat.objects.all()
        theaterID = self.request.query_params.get('theater')

        # Filter theater based on theater id
        if theaterID:
            queryset = queryset.filter(theater__id=theaterID)
        
        return queryset

class MovieList(generics.ListCreateAPIView):
    '''
    description: This API Lists and Creates Movie informations.
    parameters:
    - name: name
        type: string
        required: true
        location: body
    - name: cast
        type: string
        required: false
        location: body
    - name: director
        type: string
        required: false
        location: body
    - name: language
        type: string enum
        required: false
        location: body
    - name: run_length
        type: string
        required: false
        location: body
    - name: certificate
        type: string enum
        required: false
        location: body
    - name: image
        type: file
        required: false
        location: body
    '''

    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

class ShowList(APIView):
    '''
    description: This API Lists and Creates Shows informations. 
                 The list can be filtered using optional query paramaters like city name, theater name and movie name
    '''

    @swagger_auto_schema(manual_parameters=[city_param, movie_param, theater_param],)
    def get(self, request, format=None):
        '''
        description: This API Lists Shows informations. 
                    The list can be filtered using optional query paramaters like city name, theater name and movie name
        parameters:
        - name: city
            description: name of the city
            type: string enum
            required: false
            location: query
        - name: movie
            description: name of the movie
            type: string
            required: false
            location: query
        - name: theater
            description: name of the theater
            type: string
            required: false
            location: query
        '''
        show = self.get_queryset()
        serializer = ShowSerializer(show, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=openapi.Schema(
                             type=openapi.TYPE_OBJECT,
                             required=['version'],
                             properties={
                                 'theater': theater_body_param,
                                 'movie': movie_body_param,
                                 'showtime': showtime_body_param,
                             },
                         ),
                         operation_description='Add a Show in Theater')
    def post(self, request, format=None):
        '''
        description: This API Creates Show informations.
        parameters:
        - name: theater
            description: name of the theater
            type: string 
            required: true
            location: body
        - name: movie
            description: name of the movie
            type: string
            required: true
            location: body
        - name: showtime
            description: date and time of the show
            type: datetime
            required: true
            location: body
        '''

        try:
            if(request.data['movie'] and request.data['theater'] and request.data['showtime']):
                try:
                    movie = Movie.objects.get(name=request.data['movie'])
                except Movie.DoesNotExist:
                    return Response('Movie Not Found', status=status.HTTP_404_NOT_FOUND)

                try:
                    theater = Theater.objects.get(name=request.data['theater'])
                except Theater.DoesNotExist:
                    return Response('Theater Not Found', status=status.HTTP_404_NOT_FOUND)

                show = Show.objects.create(movie=movie, theater=theater, show_time=request.data['showtime'])
                serializer = ShowSerializer(show)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response('Inavlid parameters', status=status.HTTP_400_BAD_REQUEST)

    # Filters the queryset based on optional parameters provided
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

