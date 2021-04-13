from rest_framework import serializers
from movies.serializers import *
from booking.models import *
from datetime import datetime

class BookingSerializer(serializers.ModelSerializer):
    show = ShowSerializer(many=False)
    class Meta:
        model = Booking
        fields = '__all__'
        read_only_fields = ('created_at', 'status')
    
    def create(self, validated_data):
        print(validated_data)
        created_at = datetime.now()
        booking = Booking.objects.create(created_at=created_at, **validated_data)

        return validated_data


class ShowSeatSerializer(serializers.ModelSerializer):
    # booking = BookingSerializer(many=False)

    class Meta:
        model = ShowSeat
        fields = '__all__'
        read_only_fields = ('status', 'booking')

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'