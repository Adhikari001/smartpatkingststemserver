from django.db import models
from django.contrib.auth.models import User


class Address(models.Model):
    toleName = models.CharField(max_length=60)
    municipalityWarNo = models.SmallIntegerField()
    district = models.CharField(max_length=60)
    provinceName = models.CharField(max_length=60)
    countryName = models.CharField(max_length=60)
    modifiedDate = models.DateTimeField(auto_now=False)
    # if not permanent it is temporary address
    isPermanent = models.BooleanField()

    def __str__(self):
        return self.countryName


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    dateOfBirth = models.DateField(null=True, blank=True)
    phoneNo = models.BigIntegerField(unique=True)
    citizinshipNo = models.CharField(max_length=100, unique=True, null=True)
    isValidated = models.BooleanField(null=True)


class ParkingStation(models.Model):
    name = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()
    location = models.CharField(max_length=100, null=True)
    ip = models.CharField(max_length=45, null=True)


    def __str__(self):
        return self.name

class ParkingSpot(models.Model):
    name = models.CharField(max_length=100, unique=True)
    parkingStation = models.ForeignKey(ParkingStation, on_delete=models.CASCADE)
    occupiedBy = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, unique=False)
    reservationEndTime = models.DateTimeField(null=True)

    def __str__(self):
        return self.name


class ParkingCost(models.Model):
    name = models.CharField(max_length=100)
    parkingStation = models.OneToOneField(ParkingStation, on_delete=models.CASCADE, null=True)
    cost = models.BigIntegerField()
    minutes = models.BigIntegerField()
    minimumCost = models.BigIntegerField()

    def __str__(self):
        return self.name


class Transaction(models.Model):
    name = models.CharField(max_length=200)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    isCreditedToUser = models.BooleanField()
    amount = models.DecimalField(max_digits=14, decimal_places=4)
    productIdentity = models.CharField(max_length=500)
    productName = models.CharField(max_length=500)
    productList = models.CharField(max_length=500)
    eventHandler = models.CharField(max_length=500)
    mobile = models.CharField(max_length=20)
