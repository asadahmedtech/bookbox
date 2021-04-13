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

    # def create(self, validated_data):
    #     user = self.context['request'].user
    #     TaskProcessedData.objects.create(user=user, **validated_data)

    #     dashboard_obj = Dashboard.objects.get(user=user)
    #     dashboard_obj.pending = dashboard_obj.pending + 1
    #     dashboard_obj.save()
        
    #     print(validated_data)
    #     task = TaskPath.objects.get(taskgivenID = str(validated_data.get('taskpath')))
    #     task.taskCount = task.taskCount + 1
    #     task.save()
        
    #     return validated_data

