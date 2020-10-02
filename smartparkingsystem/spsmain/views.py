import datetime
import logging

from django.contrib.auth.models import User

from spsmain.helper import ParkingStationHelperClass

from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Transaction, ParkingSpot
from .serializers import (
    GetSpotSerializer, ParkingSpotReserveGet, UserAddSerializers)
from .userValidator import GetUserInfo


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
            flag, station = ParkingStationHelperClass.getAllNearestParkingStations(serializer)
            if flag:
                return station

            # todo get empty parking spaces from parking station using socket and validate those spot is vaccant from  db

            station_response = {'parkStaionId': 4, 'stations': {1: 1, 7: 0, 8: 1, 10: 1, 11: 0}}
            spot_detail = ParkingStationHelperClass.findParkingSpotStatus(station_response)

            return Response(spot_detail, status=status.HTTP_201_CREATED)

            # return parking station with free space

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReserveForSomeTime(APIView):
    def post(self, request):
        # serializer = Rese
        pass


class ReserveSpot(APIView):
    def post(self, request):
        print('reserve parking spot !!')
        serializer = ParkingSpotReserveGet(data=request.data)
        if (serializer.is_valid()):
            data = serializer.data
            logging.info('input data validated for reserve parking spot ', data['transactionName'])
            # getting user information
            user = GetUserInfo.getUserInformation(request.headers.get('Authorization').split()[1])

            # validating parking spot
            try:
                parkingSpot = ParkingSpot.objects.get(pk=data.get('parkingSpot'))
            except:
                return Response({"message": "not a valid parking spot"}, status=status.HTTP_400_BAD_REQUEST)

            logging.info('parking spot validated for reserve parking spot')
            # save transaction and reserve the spot
            transaction = Transaction(name=data['transactionName'], amount=data['amount'],
                                      productIdentity=data['productIdentity'],productName=data['productName'],
                                      productList=data['productList'], eventHandler=data['eventHandler'],
                                      isCreditedToUser=False, mobile=data['mobile'], user=user)
            transaction.save()

            logging.info("transaction saved for reserve parking spot")

            # parking spot reserve for user
            time = parkingSpot.reservationEndTime + datetime.timedelta(minutes=data['parkingTime'])
            parkingSpot.reservationEndTime = time
            parkingSpot.save()

            # todo response to parking station

            return Response({"Message": "Added successfully", "Reservation end time": parkingSpot.reservationEndTime,
                             "Latitude": parkingSpot.parkingStation.longitude,
                             "Longitude": parkingSpot.parkingStation.longitude,
                             "Parking station name": parkingSpot.parkingStation.name}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
