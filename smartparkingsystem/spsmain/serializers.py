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

class ParkingSpotReserveGet(serializers.ModelSerializer):
    name = serializers.CharField(max_length=200)
    amount = serializers.DecimalField(max_digits=14, decimal_places=4)
    productIdentity = serializers.CharField(max_length=500)
    productName = serializers.CharField(max_length=500)
    productList = serializers.CharField(max_length=500)
    eventHandler = serializers.CharField(max_length=500)
    mobile = serializers.IntegerField()
    parkingSpot = serializers.IntegerField()
    