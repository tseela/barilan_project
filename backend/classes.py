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
        self.googleMapsLink = str("")
        self.googleMapsImageLink = str("")
        self.orderInAdvance = bool(False)
        self.placeOfOrigin = str("")
        self.methodOfTransportation =  Transportation.NONE
        self.destination = str("")
    def __init__(self, duration, cost, timeStart, timeEnd, title, googleMapsLink, googleMapsImageLink, orderInAdvance, placeOfOrigin, methodOfTransportation, destination):
        self.duration = duration
        self.cost = cost
        self.timeStart = timeStart
        self.timeEnd = timeEnd
        self.title = title
        self.googleMapsLink = googleMapsLink
        self.googleMapsImageLink = googleMapsImageLink
        self.orderInAdvance = orderInAdvance
        self.placeOfOrigin = placeOfOrigin
        self.methodOfTransportation = methodOfTransportation
        self.destination = destination

class Transportation(Enum):
    NONE = 0
    BUS = 1
    TRAIN = 2
    RAM = 3
    PUBLICTAXI = 4

class PlaceOfStay:
    def __init__(self):
        self.duration = int(0)
        self.cost = int(0)
        self.timeStart = datetime.now()
        self.timeEnd = datetime.now()
        self.title = str("")
        self.googleMapsLink = str("")
        self.googleMapsImageLink = str("")
        self.orderInAdvance = bool(True)
        self.destination = str("")
    def __init__(self, duration, cost, timeStart, timeEnd, title, googleMapsLink, googleMapsImageLink, orderInAdvance, destination):
        self.duration = duration
        self.cost = cost
        self.timeStart = timeStart
        self.timeEnd = timeEnd
        self.title = title
        self.googleMapsLink = googleMapsLink
        self.googleMapsImageLink = googleMapsImageLink
        self.orderInAdvance = orderInAdvance
        self.destination = destination


class Activity:
    def __init__(self):
        self.duration = int(0)
        self.cost = int(0)
        self.timeStart = datetime.now()
        self.timeEnd = datetime.now()
        self.title = str("")
        self.googleMapsLink = str("")
        self.googleMapsImageLink = str("")
        self.orderInAdvance = bool(False)
    def __init__(self, duration, cost, timeStart, timeEnd, title, googleMapsLink, googleMapsImageLink, orderInAdvance):
        self.duration = duration
        self.cost = cost
        self.timeStart = timeStart
        self.timeEnd = timeEnd
        self.title = title
        self.googleMapsLink = googleMapsLink
        self.googleMapsImageLink = googleMapsImageLink
        self.orderInAdvance = orderInAdvance


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


class Trip:
    def __init__(self):
        self.duration = int(0)
        self.startDate = datetime.now()
        self.endDate = datetime.now()
        self.days = [Day()]
        self.cost = int(0)
        self.userId = int(0)
    def __init__(self, duration, startDate, endDate, days, cost, userId):
        self.duration = duration
        self.startDate = startDate
        self.endDate = endDate
        self.days = days
        self.cost = cost
        self.userId = userId