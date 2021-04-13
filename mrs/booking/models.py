from django.db import models
from movies.models import *

# Create your models here.

# Booking Model for defining the booking of shows
class Booking(models.Model):
    status = models.BooleanField(null=True, default=False)
    show = models.ForeignKey(Show, null=False, on_delete=models.CASCADE)
    user = models.CharField(max_length=100, null=True)
    created_at = models.DateTimeField()
    
    def __str__(self):
        return '{}-{}-{}-{}'.format(self.show, self.status, self.created_at, self.user)

# ShowSeat Model for defining the seats in the theaters for a given show
class ShowSeat(models.Model):
    seat = models.ForeignKey(TheaterSeat, on_delete=models.CASCADE)
    price = models.FloatField(null=False)
    status = models.BooleanField(default=False)
    show = models.ForeignKey(Show, on_delete=models.CASCADE)
    booking = models.ForeignKey(Booking, null=True ,on_delete=models.CASCADE)

    def __str__(self):
        return '{}-{}-{}-{}'.format(self.seat, self.status, self.show, self.booking)

# Payment Model for defining the payments of booking
class Payment(models.Model):
    payment_choices = (
        ('DEB','Debit Card'),
        ('CRD','Credit Card'),
        ('NET','Net Banking'),
        ('UPI','UPI'),
    )

    amount = models.FloatField(null=False)
    transactionID = models.CharField(max_length=256, null=False)
    discountID = models.CharField(max_length=256, null=False)
    created_at = models.DateTimeField()
    paymentMethod = models.CharField(max_length=3, choices=payment_choices)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)

    def __str__(self):
        return '{}-{}-{}-{}'.format(self.amount, self.transactionID, self.created_at, self.booking)

