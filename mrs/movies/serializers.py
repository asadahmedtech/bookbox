from rest_framework import serializers
from movies.models import *

class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'

class TheaterSerializer(serializers.ModelSerializer):
    city = CitySerializer(many=False, read_only=True)

    class Meta:
        model = Theater
        fields = '__all__'

class TheaterSeatSerializer(serializers.ModelSerializer):
    theater = TheaterSerializer(many=False, read_only=True)

    class Meta:
        model = TheaterSeat
        fields = '__all__'

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'

class ShowSerializer(serializers.ModelSerializer):
    theater = TheaterSerializer(many=False, read_only=True)
    movie = MovieSerializer(many=False, read_only=True)

    class Meta:
        model = Show
        fields = '__all__'
