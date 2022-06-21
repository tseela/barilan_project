from datetime import datetime
from enum import Enum
class Trip:
    def __init__(self):
        pass





class Transport:
    def __init__(self):
        self.duration = int(0)
        self.cost = int(0)
        self.timeStart = datetime.now()
        self.timeEnd = datetime.now()
        self.title = str("")
        self.originLink = str("")
        self.destinationLink = str("")
        self.orderInAdvance = bool(False)
        self.placeOfOrigin = str("")
        self.methodOfTransportation = 0
        self.destination = str("")
        self.baseStation = str("")
        self.arrivalStation = str("")
    def __init__(self, duration, cost, timeStart, timeEnd, title, originLink, destinationLink, orderInAdvance, placeOfOrigin, methodOfTransportation, destination, baseStation, arrivalStation):
        self.duration = duration
        self.cost = cost
        self.timeStart = timeStart
        self.timeEnd = timeEnd
        self.title = title
        self.originLink = originLink
        self.destinationLink = destinationLink
        self.orderInAdvance = orderInAdvance
        self.placeOfOrigin = placeOfOrigin
        self.methodOfTransportation = methodOfTransportation
        self.destination = destination
        self.baseStation = baseStation
        self.arrivalStation = arrivalStation
    def toTransport(trans):
        return Transport(trans.duration, trans.cost, trans.timeStart, trans.timeEnd, trans.title, trans.originLink, trans.destinationLink, trans.orderInAdvance, trans.placeOfOrigin, trans.methodOfTransportation, trans.destination, trans.baseStation, trans.arrivalStation)
    def __str__(self):
        return str({"Duration" : self.duration, "Cost" : self.cost, "Times:" : [self.timeStart, self.timeEnd], "Title" : self.title, "Dest" : self.destination})
    def DictToTransport(trans):
        return Transport(trans['duration'], trans['cost'], trans['timeStart'], trans['timeEnd'], trans['title'], trans['originLink'], trans['destinationLink'], trans['orderInAdvance'], trans['placeOfOrigin'], trans['methodOfTransportation'], trans['destination'], trans['baseStation'], trans['arrivalStation'])

class Transportation(Enum):
    NONE = 0
    BUS = 1
    TRAIN = 2
    RAM = 3
    PUBLICTAXI = 4
    FLIGHT = 5

class PlaceOfStay:
    def __init__(self):
        self.duration = int(0)
        self.cost = int(0)
        self.timeStart = datetime.now()
        self.timeEnd = datetime.now()
        self.title = str("")
        self.link = str("")
        self.images = str("")
        self.orderInAdvance = bool(True)
        self.destination = str("")
    def __init__(self, duration, cost, timeStart, timeEnd, title, link, images, orderInAdvance, destination):
        self.duration = duration
        self.cost = cost
        self.timeStart = timeStart
        self.timeEnd = timeEnd
        self.title = title
        self.link = link
        self.images = images
        self.orderInAdvance = orderInAdvance
        self.destination = destination
    def toPlace(place):
        return PlaceOfStay(place.duration, place.cost, place.timeStart, place.timeEnd, place.title, place.link, place.images, place.orderInAdvance, place.destination)
    def __str__(self):
        return str({"Duration" : self.duration, "Cost" : self.cost, "Times:" : [self.timeStart, self.timeEnd], "Title" : self.title, "Dest" : self.destination})
    def DictToPlace(place):
        return PlaceOfStay(place['duration'], place['cost'], place['timeStart'], place['timeEnd'], place['title'], place['link'], place['images'], place['orderInAdvance'], place['destination'])


class Activity:
    def __init__(self):
        self.duration = int(0)
        self.cost = int(0)
        self.timeStart = datetime.now()
        self.timeEnd = datetime.now()
        self.title = str("")
        self.link = str("")
        self.images = str("")
        self.orderInAdvance = bool(False)
        self.destination = str("")
    def __init__(self, duration, cost, timeStart, timeEnd, title, link, images, orderInAdvance, destination):
        self.duration = duration
        self.cost = cost
        self.timeStart = timeStart
        self.timeEnd = timeEnd
        self.title = title
        self.link = link
        self.images = images
        self.orderInAdvance = orderInAdvance
        self.destination = destination
    def insertTime(self, timeStart, timeEnd):
        self.timeStart = timeStart
        self.timeEnd = timeEnd
    def toActivity(activity):
        return Activity(activity.duration , activity.cost, activity.timeStart, activity.timeEnd, activity.title, activity.link, activity.images, activity.orderInAdvance)
    def __str__(self):
        return str({"Duration" : self.duration, "Cost" : self.cost, "Times:" : [self.timeStart, self.timeEnd], "Title" : self.title, "Dest" : self.destination})
    def DictToActivity(activity):
        return Activity(activity['duration'] , activity['cost'], activity['timeStart'], activity['timeEnd'], activity['title'], activity['link'], activity['images'], activity['orderInAdvance'], activity['destination'])


class Day:
    def __init__(self):
        self.activities = [Activity()]
        self.transportation = [Transportation()]
        self.cost = int(0)
        self.timeStart = datetime.now()
        self.timeEnd = datetime.now()
        self.duration = int(0)
        self.placeOfStay = PlaceOfStay()
    def __init__(self, activities, transportation, cost, timeStart, timeEnd, duration, placeOfStay):
        self.activities = activities
        self.transportation = transportation
        self.cost = cost
        self.timeStart = timeStart
        self.timeEnd = timeEnd
        self.duration = duration
        self.placeOfStay = placeOfStay
    def toDay(day):
        return Day(day.activities, day.transportation, day.cost, day.timeStart, day.timeEnd, day.duration, day.placeOfStay)
    def __str__(self):
        return str({"Duration" : self.duration, "Cost" : self.cost, "Times:" : [self.timeStart, self.timeEnd], "Title" : self.title, "Dest" : self.destination})
    def DictToDay(day):
        return Day(day['activities'], day['transportation'], day['cost'], day['timeStart'], day['timeEnd'], day['duration'], day['placeOfStay'])


class Trip:
    def __init__(self):
        self.name = str("")
        self.destination = str("")
        self.duration = int(0)
        self.startDate = datetime.now()
        self.endDate = datetime.now()
        self.days = [Day()]
        self.cost = int(0)
        self.userId = int(0)
        self.initFlight = [Transport()]
        self.finFlight = [Transport()]
    def __init__(self, name, destination, duration, startDate, endDate, days, cost, userId, initFlight, finFlight):
        self.name = name
        self.destination = destination
        self.duration = duration
        self.startDate = startDate
        self.endDate = endDate
        self.days = days
        self.cost = cost
        self.userId = userId
        self.initFlight = initFlight
        self.finFlight = finFlight
    def toTrip(trip) -> Trip:
        return Trip(trip.name, trip.destination, trip.duration, trip.startDate, trip.endDate, trip.days, trip.cost, trip.userId, trip.initFlight, trip.finFlight)
    def __str__(self):
        return str({"Duration" : self.duration, "Cost" : self.cost, "Times:" : [self.startDate, self.endDate], "Name" : self.name, "Dest" : self.destination})
    def DictToTrip(trip) -> Trip:
        return Trip(trip['name'], trip['destination'], trip['duration'], trip['startDate'], trip['endDate'], trip['days'], trip['cost'], trip['userId'], trip['initFlight'], trip['finFlight'])