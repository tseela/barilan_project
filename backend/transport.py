import requests
import json
import ast
# from algo.libs.classes import Transport
import classes
from datetime import datetime

class transportFunctions:
    def __init__(self):
        pass


    def getTransport(self, latitude1, longitude1, latitude2, longitude2):
        # get transport between 2 places
        origin = str(latitude1) + "," + str(longitude1)
        destination = str(latitude2) + "," + str(longitude2)
        url = "https://transit.router.hereapi.com/v8/routes?apiKey=pGwbEV9EnOVSNh94i8prG-B4oBd8RSO8bP6lk_u6NXI&origin=" + origin + "&destination=" + destination

        response = requests.get(url)
        trans = ast.literal_eval(response.text)

        if len(trans["routes"]) == 0:
            return []

        way = trans["routes"][0]

        sections = way["sections"]


        # create object for every transportation
        transportations = []
        for section in sections:
            transResults = self.createTransportation(section)
            transportations.append(transResults)
        

        # add the destinations to walks
        length = len(transportations)
        for index in range(length):
            trans = transportations[index]
            if (trans.title == "pedestrian"):
                if (index + 1 < length):
                    trans.arrivalStation = transportations[index + 1].baseStation

                if (index != 0):
                    trans.baseStation = transportations[index - 1].arrivalStation


        return transportations
    


    def getTransportByTime(self, latitude1, longitude1, latitude2, longitude2, depTime):
        # get transport bewtween 2 places on another time
        origin = str(latitude1) + "," + str(longitude1)
        destination = str(latitude2) + "," + str(longitude2)
        url = "https://transit.router.hereapi.com/v8/routes?apiKey=pGwbEV9EnOVSNh94i8prG-B4oBd8RSO8bP6lk_u6NXI&origin=" + origin + "&destination=" + destination + "&departureTime=" + depTime

        response = requests.get(url)
        trans = ast.literal_eval(response.text)

        if len(trans["routes"]) == 0:
            return []

        way = trans["routes"][0]

        sections = way["sections"]


        # create object for every transportation
        transportations = []
        for section in sections:
            transResults = self.createTransportation(section)
            transportations.append(transResults)


        # add the destinations to walks
        length = len(transportations)
        for index in range(length):
            trans = transportations[index]
            if (trans.title == "pedestrian"):
                if (index + 1 < length):
                    trans.arrivalStation = transportations[index + 1].baseStation

                if (index != 0):
                    trans.baseStation = transportations[index - 1].arrivalStation

        return transportations



    def createTransportation(self, section):
        # create transportation object
        mode = section["type"]

        cost = None

        transType = 0
        order = False


        # create the prices and types
        baseStation = ""
        arrivalStation = ""
        if mode == "pedestrian":
            cost = 0

        else:
            mode = section["transport"]["mode"]
            if mode == "bus":
                transType = 1
                cost = 6
            elif mode == "regionalTrain":
                transType = 2
                cost = 40
            elif mode == "subway":
                transType = 3
                cost = 10

            baseStation = section["departure"]["place"]["name"]
            arrivalStation = section["arrival"]["place"]["name"]


        # get the times
        startTime = section["departure"]["time"].split("+")[0]
        if (len(section["departure"]["time"].split("-")) == 4):
            startTime = '-'.join(section["departure"]["time"].split("-")[:-1])
        startTime = datetime.strptime(startTime, '%Y-%m-%dT%H:%M:%S')
        startPlace = str(section["departure"]["place"]["location"]["lat"]) + "," + str(section["departure"]["place"]["location"]["lng"])


        endTime = section["arrival"]["time"].split("+")[0]
        if (len(section["arrival"]["time"].split("-")) == 4):
            endTime = '-'.join(section["arrival"]["time"].split("-")[:-1])
        endTime = datetime.strptime(endTime, '%Y-%m-%dT%H:%M:%S')
        endPlace = str(section["arrival"]["place"]["location"]["lat"])+ "," + str(section["arrival"]["place"]["location"]["lng"])


        duration = int((endTime - startTime).total_seconds())/3600

        googleMaps = "https://www.google.com/maps/@" + startPlace + ",17z"
        googleMaps2 = "https://www.google.com/maps/@" + endPlace + ",17z"
        transportation = classes.Transport(duration, cost, startTime, endTime, mode, googleMaps, googleMaps2, order, startPlace, transType, endPlace, baseStation, arrivalStation)

        return transportation



# get geocode of a place
def getNZfromCity(city):
    url = "http://api.positionstack.com/v1/forward?access_key=e40fa43000e24098607004614faabc0f&query=" + city
    response = requests.get(url)

    response = json.loads(response.text)
     
    latitude = float(response["data"][0]["latitude"])
    longitude = float(response["data"][0]["longitude"])

    return latitude, longitude
    
