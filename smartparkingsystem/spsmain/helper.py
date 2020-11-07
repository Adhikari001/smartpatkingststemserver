import pickle
import math
import socket

from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response
from threading import Thread

from spsmain.models import ParkingSpot, ParkingStation

status = []

class ParkingStationHelperClass:

    @staticmethod
    def sortFunction(e):
        return e['distance']

    @staticmethod
    def findParkingSpotStatus(stationResponses):
        response = []
        for stationResponse in stationResponses:
            try:
                parking_station = ParkingStation.objects.get(pk=stationResponse.get('parkStaionId'))
            except:
                return Response({"error!!": "parking station does not exist"},
                                status=status.HTTP_400_BAD_REQUEST)
            stations = stationResponse.get('stations')
            # parking_status = []
            # for station in stations:
            #     if stations[station] == 1:
            #         try:
            #             parking_spot = ParkingSpot.objects.get(pk=station)
            #         except:
            #             return Response({"error!!": "parking spot does not exist"},
            #                             status=status.HTTP_400_BAD_REQUEST)
            #         time = parking_spot.reservationEndTime
            #         if time < timezone.now() :
            #             spot_detail = {"parking_station":self.prepareParkingStation(parking_station), "parking_spot":self.prepareParkingSpot(parking_spot)}
            #             vaccantStations.append(spot_detail)
            spot = []
            for station in stations:
                try:
                    parking_spot = ParkingSpot.objects.get(pk=station)
                except:
                    return Response({"error!!": "parking spot does not exist"},
                                    status=status.HTTP_400_BAD_REQUEST)
                time = parking_spot.reservationEndTime
                occupied_by_vehicle = bool(stations[station])
                occupied_by_time = time > timezone.now()

                spot_detail = ParkingStationHelperClass.prepareParkingSpot(parking_spot, occupied_by_time,
                                                                           occupied_by_vehicle)
                spot.append(spot_detail)

            response.append(ParkingStationHelperClass.prepareParkingStation(parking_station, spot))
        return response

    @staticmethod
    def prepareParkingSpot(parkingSpot, occupiedByTime, occupiedByVehicle):
        return {"id": parkingSpot.id, "name": parkingSpot.name,
                "occupiedByVehicle": occupiedByVehicle, "occupiedByTime": occupiedByTime}

    @staticmethod
    def prepareParkingStation(parkingStation, spot):
        return {"id": parkingStation.id, "name": parkingStation.name, "latitude": parkingStation.latitude,
                "longitude": parkingStation.longitude, "location": parkingStation.location,"cost": parkingStation.parkingcost.cost,
                "minutes":parkingStation.parkingcost.minutes, "minimum cost": parkingStation.parkingcost.minimumCost, "distance": 1000,
                "parkingSpot": spot}

    @staticmethod
    def getAllNearestParkingStations(serializer):

        user_request = serializer.data
        req_lat = math.radians(user_request.get('latitude'))
        req_lon = math.radians(user_request.get('longitude'))
        distance = user_request.get('distance')
        # get all parking station from db
        parking_stations = ParkingStation.objects.all()
        valid_station = []
        counter = 0
        for parkingStation in parking_stations:
            lat = math.radians(parkingStation.latitude)
            lon = math.radians(parkingStation.longitude)
            d = ParkingStationHelperClass.haversine(lat, lon, req_lat, req_lon)

            if d <= distance:
                station = {'station': parkingStation, 'distance': d}
                valid_station.append(station)
                counter += 1
                print("found station", parkingStation.name)

        if counter == 0:
            return True, Response({"error!!": "parking station not found within the given distance"},
                            status=status.HTTP_400_BAD_REQUEST)

        # validStation.sort(key=self.sortFunction)
        return False, valid_station

    @staticmethod
    def haversine(lat1, lon1, lat2, lon2):

        # distance between latitudes
        # and longitudes
        dLat = (lat2 - lat1)
        dLon = (lon2 - lon1)

        # apply formulae
        a = (pow(math.sin(dLat / 2), 2) + pow(math.sin(dLon / 2), 2) * math.cos(lat1) * math.cos(lat2));
        rad = 6371000
        c = 2 * math.asin(math.sqrt(a))
        return rad * c


global status

def findStationStatus(IP, PORT):
    user_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    user_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    user_socket.connect((IP, PORT))

    d = {"findparkingSpot": 1}
    user_socket.send(pickle.dumps(d))

    response = user_socket.recv(112)
    status.append(pickle.loads(response))
    #user_socket.close()

def findStationsStatus(stations):
    status = []
    threads = []
    for station in stations:
        t = Thread(target=findStationStatus, args= (station.ip, station.port))
        t.start()
        threads.append(t)
        pass

    for thread in threads:
        thread.join()
    return status


def reserveSpot(IP, PORT, spot, time, vehicleNo):
    user_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    user_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    user_socket.connect((IP, PORT))

    spot_req = { "spot": spot, "time": time, "vehicleNo": vehicleNo}
    msg = pickle.dumps(spot_req)
    user_socket.send(msg)

    response = user_socket.recv(112)
    #user_socket.close()

    #confirmation = {"parkingstation_id":0,"spot":r_spot,"reserve":1,"time":r_time}
    return pickle.loads(response)


