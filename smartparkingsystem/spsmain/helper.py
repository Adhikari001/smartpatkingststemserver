import math

from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response

from spsmain.models import ParkingSpot, ParkingStation


class ParkingStationHelperClass:

    @staticmethod
    def sortFunction(e):
        return e['distance']

    @staticmethod
    def findEmptySpot(stationResponse):
        try:
            parkingStation = ParkingStation.objects.get(pk=stationResponse.get('parkStaionId'))
        except:
            print("parking station does not exist")
            return Response({"error!!": "parking station does not exist"},
                            status=status.HTTP_400_BAD_REQUEST)
        stations = stationResponse.get('stations')
        vaccantStations = []
        # for station in stations:
        #     if stations[station] == 1:
        #         try:
        #             parkingSpot = ParkingSpot.objects.get(pk=station)
        #         except:
        #             print('Parking spot does not exist')
        #             return Response({"error!!": "parking spot does not exist"},
        #                             status=status.HTTP_400_BAD_REQUEST)
        #         time = parkingSpot.reservationEndTime
        #         if time < timezone.now() :
        #             spotDetail = {"parkingStation":self.prepareParkingStation(parkingStation), "parkingSpot":self.prepareParkingSpot(parkingSpot)}
        #             vaccantStations.append(spotDetail)

        for station in stations:
            try:
                parkingSpot = ParkingSpot.objects.get(pk=station)
            except:
                print('Parking spot does not exist')
                return Response({"error!!": "parking spot does not exist"},
                                status=status.HTTP_400_BAD_REQUEST)
            time = parkingSpot.reservationEndTime
            occupiedByVehicle = bool(stations[station])
            occupiedByTime = time < timezone.now()

            spotDetail = {"parkingStation": ParkingStationHelperClass.prepareParkingStation(parkingStation),
                          "parkingSpot": ParkingStationHelperClass.prepareParkingSpot(parkingSpot, occupiedByTime, occupiedByVehicle)}
            vaccantStations.append(spotDetail)

        return vaccantStations

    @staticmethod
    def prepareParkingSpot(parkingSpot, occupiedByTime, occupiedByVehicle):
        return {"id": parkingSpot.id, "name": parkingSpot.name,
                "occupiedByVehicle": occupiedByVehicle, "occupiedByTime": occupiedByTime}

    @staticmethod
    def prepareParkingStation(parkingStation):
        return {"id": parkingStation.id, "name": parkingStation.name, "latitude": parkingStation.latitude,
                "longitude": parkingStation.longitude, "location": parkingStation.location, "distance": 1000}

    @staticmethod
    def getAllNearestParkingStations(serializer):

        userRequest = serializer.data
        reqLat = math.radians(userRequest.get('latitude'))
        reqLon = math.radians(userRequest.get('longitude'))
        distance = userRequest.get('distance')
        # get all parking station from db
        parkingStations = ParkingStation.objects.all()
        validStation = []
        counter = 0
        for parkingStation in parkingStations:
            lat = math.radians(parkingStation.latitude)
            lon = math.radians(parkingStation.longitude)
            # haversine formula
            alph = (math.sin(lat) * math.sin(reqLat)) + (2 * math.cos(lat) * math.cos(reqLat) * math.cos(lon - reqLon))
            d = 6371000 * alph

            print("Distance is:",d)
            if d <= distance:
                print("inside the required distance")
                station = {'station': parkingStation, 'distance': alph}
                validStation.append(station)
                counter += 1
        if(len(validStation)==0):

            print("inside if 12345")
            return Response({"error!!": "parking station not found within the given diatance"},
                            status=status.HTTP_400_BAD_REQUEST)
        # validStation.sort(key=self.sortFunction)
        print(validStation)
        return validStation
