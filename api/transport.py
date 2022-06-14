import requests
import json
import ast
# from algo.libs.classes import Transport
import classes
from datetime import datetime


def getTransport(latitude1, longitude1, latitude2, longitude2):
    origin = str(latitude1) + "," + str(longitude1)
    destination = str(latitude2) + "," + str(longitude2)
    url = "https://transit.router.hereapi.com/v8/routes?apiKey=pGwbEV9EnOVSNh94i8prG-B4oBd8RSO8bP6lk_u6NXI&origin=" + origin + "&destination=" + destination

    response = requests.get(url)
    trans = ast.literal_eval(response.text)

    way = trans["routes"][0]

    sections = way["sections"]


    transportations = []
    for section in sections:
        transportations.append(createTransportation(section))


    return transportations
        

def createTransportation(section):
    mode = section["type"]

    cost = None
    transType = classes.Transportation.NONE
    order = False
    if mode == "pedestrian":
        cost = 0

    else:
        mode = section["transport"]["mode"]
        if mode == "bus":
            transType = classes.Transportation.BUS


    startTime = section["departure"]["time"].split("+")[0]
    startTime = datetime.strptime(startTime, '%Y-%m-%dT%H:%M:%S')
    startPlace = str(section["departure"]["place"]["location"]["lat"]) + "," + str(section["departure"]["place"]["location"]["lng"])


    endTime = section["arrival"]["time"].split("+")[0]
    endTime = datetime.strptime(endTime, '%Y-%m-%dT%H:%M:%S')
    endPlace = str(section["arrival"]["place"]["location"]["lat"])+ "," + str(section["arrival"]["place"]["location"]["lng"])


    duration = endTime - startTime

    googleMaps = "https://www.google.com/maps/@" + startPlace + ",17z"
    googleMaps2 = "https://www.google.com/maps/@" + endPlace + ",17z"
    transportation = classes.Transport(duration, cost, startTime, endTime, mode, googleMaps, googleMaps2, order, startPlace, transType, endPlace)

    return transportation






# url = "https://transit.router.hereapi.com/v8/routes?apiKey=pGwbEV9EnOVSNh94i8prG-B4oBd8RSO8bP6lk_u6NXI&origin=41.79457,12.25473&destination=41.90096,12.50243"
# url = "https://transit.router.hereapi.com/v8/routes?apiKey=pGwbEV9EnOVSNh94i8prG-B4oBd8RSO8bP6lk_u6NXI&origin=32.0845191,34.8037962&destination=32.0791345,34.7924341"



# response = requests.get(url)

# # print(response.text)
# # print(dict(response.text))
# d = ast.literal_eval(response.text)

# print(json.dumps(d, sort_keys=False, indent=4))
# print(response.__dict__)

tr = getTransport(32.0845191,34.8037962,32.0791345,34.7924341)
print(tr)
for t in tr:
    for a in t.__dict__:
        print(t.__dict__[a])
    # print(json.dumps(t.__dict__, sort_keys=False, indent=4))