import math
import datetime

from django.contrib.auth.models import User
from django.utils import timezone

from spsmain.helper import ParkingStationHelperClass

from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.serializers import VerifyJSONWebTokenSerializer

from .models import ParkingStation, ParkingSpot
from .serializers import GetSpotSerializer, TransactionAddSerializer, UserAddSerializers, ParkingSpotReserveGet
from .userValidator import Validate


@permission_classes((AllowAny,))
class CreateUser(APIView):
    def post(self, request):
        serializer = UserAddSerializers(data=request.data)
        if (serializer.is_valid()):
            user = serializer.data
            User.objects.create_user(user.get('username'), password=user.get('password'),
                                     first_name=user.get('first_name'),
                                     last_name=user.get('last_name'), email=user.get('email'))
            # serializer.save()
            return Response({'username': user.get('username'), 'email': user.get('email'),
                             'first_name': user.get('first_name'), 'last_name': user.get('last_name')},
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetVacantSpot(APIView):
    def post(self, request):
        # request vacant spot
        serializer = GetSpotSerializer(data=request.data)
        if serializer.is_valid():
            # find parking station
            station =  ParkingStationHelperClass.getAllNearestParkingStations(serializer)

            # get empty parking spaces from parking station using socket and validate those spot is vaccant from  db
            stationResponse={'parkStaionId':4, 'stations':{1:1, 7:0, 8:1, 10:1, 11:0}}
            spotDetail = ParkingStationHelperClass.findEmptySpot(stationResponse)

            return Response(spotDetail, status=status.HTTP_201_CREATED)

            # return parking station with free space

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReserveSpot(APIView):
    def post(self, request):
        user = Validate.getValidate(request)
        serializer = ParkingSpotReserveGet(data=request.data)
        if (serializer.is_valid()):
            data = serializer.data
            # save transaction and reserve the spot

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



