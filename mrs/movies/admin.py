from django.contrib import admin
from movies.models import *

# Register your models here.
admin.site.register(City)
admin.site.register(Theater)
admin.site.register(TheaterSeat)
admin.site.register(Movie)
admin.site.register(Show)