from django.shortcuts import render
from movies.models import *
from movies.serializers import *
from rest_framework import generics

# Create your views here.
class CityList(generics.ListCreateAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer

class TheaterList(generics.ListCreateAPIView):
    model = Theater
    serializer_class = TheaterSerializer

    def get_queryset(self):
        queryset = Theater.objects.all()
        cityID = self.request.query_params.get('city')
        movieID = self.request.query_params.get('movie')

        if cityID:
            queryset = queryset.filter(city=cityID)
        if movieID:
            showqueryset = Show.objects.all()
            showqueryset = showqueryset.filter(movie=movieID).values_list('theater__id', flat=True)
            queryset = queryset.filter(id__in=showqueryset)
        
        return queryset

class MovieList(generics.ListCreateAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

class ShowList(generics.ListCreateAPIView):
    queryset = Show.objects.all()
    serializer_class = ShowSerializer

    def get_queryset(self):
        queryset = Show.objects.all()
        cityID = self.request.query_params.get('city')
        theaterID = self.request.query_params.get('theater')
        movieID = self.request.query_params.get('movie')

        if movieID:
            queryset = queryset.filter(movie=movieID)
        if theaterID:
            queryset = queryset.filter(theater=theaterID)
        if cityID:
            queryset = queryset.filter(theater__city=cityID)
        
        return queryset

