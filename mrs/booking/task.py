from __future__ import absolute_import
from django.db import transaction
from celery import shared_task

from booking.models import *

@shared_task
def unbook_seat_task(bookingID):
    print("Unbooking now")
    try:
        booking = Booking.objects.get(pk=bookingID)
        if(booking.status):
            print("Payment Success")
            return
        
        #Unreserving tickets
        print("Unreserving Seats")
        with transaction.atomic():
            ShowSeat.objects.filter(booking=booking.id).update(status=False)
            ShowSeat.objects.filter(booking=booking.id).update(booking=None)
        
        return

    except Booking.DoesNotExist:
        print("Invalid BookingID")
        return