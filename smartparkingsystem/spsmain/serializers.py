from rest_framework import serializers
from django.contrib.auth.models import User

from .models import Transaction

class UserAddSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username','first_name', 'last_name', 'email', 'password']


class TransactionAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['name', 'amount', 'last_name', 'email', 'password']

class GetSpotSerializer(serializers.Serializer):
    latitude = serializers.FloatField(allow_null=False, max_value=90 , min_value= -90)
    longitude = serializers.FloatField(allow_null=False, max_value= 180, min_value= -180)
    distance = serializers.IntegerField(allow_null=False)

class ParkingSpotReserveGet(serializers.Serializer):
    transactionName = serializers.CharField(max_length=200)
    amount = serializers.DecimalField(max_digits=14, decimal_places=4)
    productIdentity = serializers.CharField(max_length=500)
    productName = serializers.CharField(max_length=500)
    productList = serializers.CharField(max_length=500)
    eventHandler = serializers.CharField(max_length=500)
    mobile = serializers.IntegerField()
    parkingSpot = serializers.IntegerField()
    parkingTime = serializers.IntegerField()


class ReserveForTransaction(serializers.Serializer):
    spotId = serializers.IntegerField(allow_null=False)


class UserGetDetailSerializer(serializers.Serializer):
    permanentToleName = serializers.CharField(max_length=60, allow_null=True)
    permanentMunicipalityWarNo = serializers.IntegerField(max_value=50, allow_null= True)
    permanentDistrict = serializers.CharField(max_length=60, allow_null=True)
    permanentProvinceName = serializers.CharField(max_length=60, allow_null=True)
    permanentDistrictCountryName = serializers.CharField(max_length=60, allow_null=True)

    temporaryToleName = serializers.CharField(max_length=60, allow_null=True)
    temporaryMunicipalityWarNo = serializers.IntegerField(max_value=50, allow_null= True)
    temporaryDistrict = serializers.CharField(max_length=60, allow_null=True)
    temporaryProvinceName = serializers.CharField(max_length=60, allow_null=True)
    temporaryCountryName = serializers.CharField(max_length=60, allow_null=True)

    dateOfBirth = serializers.DateField()
    phoneNo = serializers.IntegerField()
    citizenship = serializers.CharField(max_length=100)

