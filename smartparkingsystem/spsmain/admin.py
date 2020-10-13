from django.contrib import admin
from .models import ParkingStation, ParkingCost,  ParkingSpot
# Register your models here.

admin.site.register(ParkingStation)
admin.site.register(ParkingCost)
admin.site.register(ParkingSpot)
