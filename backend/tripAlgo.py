#!/usr/bin/env python
# coding: utf-8

# In[1]:


from classes import Trip
from flights import Flights
from amadeus import Client, ResponseError
from datetime import timedelta, date
import datetime
from hotels1 import hotelFunctions
from transport import transportFunctions
from transport import getNZfromCity
from amadeus import Location
import random
from classes import Day
import time

def cleanUsedAttractions(attractions, usedAttractions):

    newAttractionList = []
    
    for i in attractions:
        if (i.title.lower() in usedAttractions):
            continue
        newAttractionList.append(i)
        
    return newAttractionList

def getLandingDate(initFlight):

    relevantFlight = initFlight[-1]
    return relevantFlight.timeEnd
    
def getDepartureDate(finFlight):

    relevantFlight = finFlight[0]
    return relevantFlight.timeStart

def chooseCheapestHotel(hotels):

    lowest = 1000000
    index = 0
    
    for i in range(0, len(hotels)):
        if (hotels[i].cost < lowest):
            index = i
            lowest = hotels[i].cost
            
    return hotels[index]
    
def chooseMostLuxuriousHotel(hotels):

    highest = 0
    index = 0
    
    for i in range(0, len(hotels)):
        if (hotels[i].cost > highest):
            index = i
            highest = hotels[i].cost
            
    return hotels[index]
    
def chooseHotel(lowCost, luxury, hotelObject, city, passengerCount):

    print(getNZfromCity(city)[0], getNZfromCity(city)[1])
    xCoord = getNZfromCity(city)[0]
    yCoord = getNZfromCity(city)[1]
    hotels = []
    nxCoord = xCoord
    nyCoord = yCoord
    while (hotels == []):
        hotels = hotelObject.getHotelsByGeocode(nxCoord, nyCoord)
        print("Hotel results are", hotels, nxCoord, nyCoord)
        nxCoord = xCoord + (random.random() - 0.5) * 0.1
        nyCoord = yCoord + (random.random() - 0.5) * 0.1
        
    print(hotels)
    
    for i in hotels:
        print(i)
        
    choosenHotel = None
    
    if (lowCost):
        choosenHotel = chooseCheapestHotel(hotels)
    elif (luxury):
        choosenHotel = chooseMostLuxuriousHotel(hotels)
    else:
        choosenHotel = random.choice(hotels)
        
    choosenHotel.cost = choosenHotel.cost * passengerCount
    
    return choosenHotel

def planDay(fastPaced, attractionOptions, transportObject, xCoord, yCoord, date, usedAttractions, passengerCount, hotel, currDate = [], attractionCount = 2):

    if (currDate == []):
        currDate = date.replace(minute = 0, hour = 9, second=0)
        
    startingDate = currDate
    print("THE DATE IS:", currDate)
    attractionArr = []
    transportArr = []
    currX = xCoord
    currY = yCoord
    
    if (fastPaced and attractionCount == 2):
        
        attractionCount = 3
        
    totalCost = 0
    hotelTitle = hotel.title
    currTitle = hotelTitle
    
    for i in range(0, min((attractionCount), len(attractionOptions))):
        
        attractionLocation = attractionOptions[i].destination.split(',')
        destX = float(attractionLocation[0])
        destY = float(attractionLocation[1])
        currTransport = transportObject.getTransportByTime(currX, currY, destX, destY, str(currDate.isoformat()))
        
        if (currTransport != []):
            
            currTransport[0].baseStation = currTitle
            currTransport[-1].arrivalStation = attractionOptions[i].title
            
        currX = destX
        currY = destY
        currTitle = attractionOptions[i].title
        
        for trans in currTransport:
            
            if (trans.cost != None):
                trans.cost = trans.cost * passengerCount
                totalCost += trans.cost
                
        print(currTransport)
        print("ATTRACTIONS ARE", attractionArr)
        currDate = currTransport[-1].timeEnd
        currDate = currDate + datetime.timedelta(minutes=5)
        transportArr.append(currTransport)
        attractionOptions[i].timeStart = currDate
        currDate = currDate + datetime.timedelta(hours=3)
        attractionOptions[i].timeEnd = currDate
        currDate = currDate + datetime.timedelta(minutes=60)
        attractionOptions[i].cost = attractionOptions[i].cost * passengerCount
        totalCost += attractionOptions[i].cost
        attractionArr.append(attractionOptions[i])
        usedAttractions.append(attractionOptions[i].title.lower())
        
    print("The date at the end is", currDate)
    currTransport = transportObject.getTransportByTime(currX, currY, xCoord, yCoord, str(currDate.isoformat()))
    currTransport[0].baseStation = currTitle
    currTransport[-1].arrivalStation = hotelTitle
    
    for trans in currTransport:
        
        if (trans.cost != None):
            trans.cost = trans.cost * passengerCount
            totalCost += trans.cost
            
    transportArr.append(currTransport)
    print("Found Attractions:\n\n\n")
    
    for i in attractionArr:
        print(i)
        
    print("Found Trip\n\n\n")
    
    for i in transportArr:
        for j in i:
            print(j)
    totalCost += hotel.cost
    
    return Day(attractionArr, transportArr, totalCost, startingDate, currTransport[-1].timeEnd, 0, hotel), usedAttractions

def planFullDay(tripPeople, luxury, lowCost, museumOriented, 
                fastPaced, priceCapLeft, attractionObject, transportObject, hotel, usedAttractions, date):
    
    xCoord = hotel.destination.split(',')
    originalYCoord = float(xCoord[1])
    originalXCoord = float(xCoord[0])
    xCoord = originalXCoord
    yCoord = originalYCoord
    print(xCoord, yCoord)
    attractions = [] # maybe add most_central_location implementation later
    print("STARTING FULL DAY") 
    retries = 0
    
    while ((attractions == [] or len(attractions) < 3) and not retries == 20):
        
        print("BEFORE ATTRACTIONS")
        attractions = attractionObject.getActivities(xCoord, yCoord, 10)
        print("AFTER ATTRACTIONS", attractions)
        attractions = cleanUsedAttractions(attractions, usedAttractions)
        print("AFTER CLEAN", attractions)
        print("Coords are", xCoord, yCoord)
        noise = (random.random() - 0.5) * 0.4
        xCoord += noise
        yCoord += noise
        retries += 1
        
    attractionOptions = []
    
    for i in attractions:
        print(i)
    
    if (museumOriented):
    
        for i in attractions:
            
            if ('museum' in i.title.lower()):
                
                attractionOptions.append(i)
                
        if (attractionOptions == []):
            
            attractionOptions = attractions
            noise = (random.random() - 0.5) * 0.2
            xCoord += noise
            yCoord += noise
            
    else:
        
        attractionOptions = attractions
        
    if (lowCost):
        
        attractionOptions.sort(key=lambda x: x.cost)
        
    elif (luxury):
        
        attractionOptions.sort(key=lambda x: x.cost, reverse=True)
        
    day, usedAttractions = planDay(fastPaced, attractionOptions, transportObject, originalXCoord, originalYCoord, date, usedAttractions, tripPeople, hotel)
    
    return day, usedAttractions

def createArrivalDay(airportCoords, hotel, amadeusObject, arrivalTime, usedAttractions, hotelObject, luxury, lowCost, museumOriented, fastPace, passengerCount):
    
    print("cccccccccccccccccc")
    coords = hotel.destination.split(',')
    hotelXCoord = coords[0]
    hotelYCoord = coords[1]
    arrivalTime = arrivalTime + datetime.timedelta(hours=2) 
    exitTime = arrivalTime.isoformat()
    transportObject = transportFunctions()
    print("zzzzzzzzzzzzzzz")
    airportToHotel = transportObject.getTransportByTime(airportCoords[0], airportCoords[1], hotelXCoord, hotelYCoord, exitTime)
    airportToHotel[0].departureStation = "Airport"
    airportToHotel[-1].arrivalStation = hotel.title
    print(",,,,,,,,,,,,,,,,,,,,")
    
    for trans in airportToHotel:
        
        print(trans)
        
        if (trans.cost != None):
            
            trans.cost = trans.cost * passengerCount
            
    hotelArrivalTime = airportToHotel[-1].timeEnd
    print(hotelArrivalTime)
    hotelArrivalTime += datetime.timedelta(hours=2)
    
    if (hotelArrivalTime.time().hour < 18):
        
        hotelArrivalTime = hotelArrivalTime.replace(hour = max(hotelArrivalTime.time().hour, 9))
        attractions = hotelObject.getActivities(hotel.destination.split(',')[0], hotel.destination.split(',')[1], 2)
        plannedDay, usedAttractions = planDay(False, attractions, transportObject, hotelXCoord, hotelYCoord, hotelArrivalTime, [], passengerCount, hotel, currDate=hotelArrivalTime, attractionCount = 1)
        plannedDay.transportation.append(airportToHotel)
        
    else:
        
        usedAttractions = []
        plannedDay = Day([], [airportToHotel], hotel.cost, arrivalTime, airportToHotel[-1].timeEnd, 0, hotel)
        
    print("In create arrival day:")
    print(airportToHotel)
    
    for i in airportToHotel:
        
        print(i)
        
    return plannedDay, usedAttractions
    
def createDepartureDay(airportCoords, hotel, amadeusObject, departureTime, usedAttractions, hotelObject, luxury, lowCost, museumOriented, fastPace, passengerCount):

    coords = hotel.destination.split(',')
    hotelXCoord = coords[0]
    hotelYCoord = coords[1]
    departureTime = departureTime + datetime.timedelta(hours=6) 
    exitTime = departureTime.isoformat()
    transportObject = transportFunctions()
    hotelToAirport = transportObject.getTransportByTime(hotelXCoord, hotelYCoord, airportCoords[0], airportCoords[1], exitTime)
    hotelToAirport[0].departureStation = hotel.title
    hotelToAirport[-1].arrivalStation = 'Airport'
    totalCost = 0
    for trans in hotelToAirport:
        if (trans.cost != None):
            trans.cost = trans.cost * passengerCount
            totalCost += trans.cost
            
    airportArrivalTime = hotelToAirport[-1].timeEnd
    plannedDay = Day([], [hotelToAirport], totalCost + hotel.cost, exitTime, departureTime, 0, hotel)
    return plannedDay # this could be a future problem

# In[2]:


def getTrip(srcAirport, date, duration, passengerCount, isFastPaced, isMuseumOriented, isLuxury, isLowCost, city):

    amadeusBaseObject = Client(
    client_id='1HFEm5VJHmwxKFasVo2oSmYwnzyryeM2',
    client_secret='RNnBNiBHo6olo9tC'
    )
    
    duration -= 1
    
    flightObject = Flights(amadeusBaseObject)
    nearestAirport = amadeusBaseObject.reference_data.locations.get(
    keyword=city,
    subType=Location.ANY
    )
    
    nearestAirport = nearestAirport.data
    destinationAirport = nearestAirport[0]['iataCode']
    coordsArr = [nearestAirport[0]['geoCode']['latitude'], nearestAirport[0]['geoCode']['longitude']]
    initFlight = flightObject.getFlightObjects(srcAirport, destinationAirport, date, passengerCount)
    landingDate = str(getLandingDate(initFlight)).split(' ')[0]
    dateFormat = '%Y-%m-%d' 
    dateObject = datetime.datetime.strptime(landingDate, dateFormat)
    finFlight = flightObject.getFlightObjects(destinationAirport, srcAirport, (dateObject + timedelta(days=duration)).strftime("%Y-%m-%d"), passengerCount)
    tripStartTime = getLandingDate(initFlight)
    tripEndTime = getDepartureDate(finFlight)
    hotelObject = hotelFunctions(amadeusBaseObject)
    hotel = chooseHotel(isLowCost, isLuxury, hotelObject, city, passengerCount)
    print(hotel)
    attractions = hotelObject.getActivities(hotel.destination.split(',')[0], hotel.destination.split(',')[1], 2)
    currDate = tripStartTime
    usedAttractions = []
    dayArr = []
    
    while (currDate.date() != tripEndTime.date()):
    
        print("THIS IS THE DATES", currDate.date(), tripEndTime.date())
        
        if (currDate == tripStartTime):
            results = createArrivalDay(coordsArr, hotel, amadeusBaseObject, tripStartTime, usedAttractions, hotelObject, isLuxury, isLowCost, isMuseumOriented, isFastPaced, passengerCount)
            print("Creating arrival day")
            dayArr.append(results[0])
            usedAttractions = results[1]
            
        else:
            print("HHHHHHHHHHHHHHHH")
            transport = transportFunctions()
            print("XXXXXXXXXXXXXX")
            results = planFullDay(passengerCount, isLuxury, isLowCost, isMuseumOriented, isFastPaced, 10000, hotelObject, transport, hotel, usedAttractions, currDate)
            print("GGGGGGGGGGGGGGGGGGGGGGGG")
            print("Creating regular day")
            dayArr.append(results[0])
            usedAttractions = results[1]
            
        currDate = currDate + timedelta(days=1)
        
    print(attractions)
    lastDay = createDepartureDay(coordsArr, hotel, amadeusBaseObject, tripEndTime, usedAttractions, hotelObject, isLuxury, isLowCost, isMuseumOriented, isFastPaced, passengerCount)
    dayArr.append(lastDay)
    tripObject = Trip("Tripping like a trip", city, duration, initFlight[0].timeStart, finFlight[-1].timeEnd, dayArr, 0, '5', initFlight, finFlight)
    print(tripObject)
    
    return tripObject


def switchingTripActivities(tripObject):
    transportObject = transportFunctions()
    newTrip = deepcopy(tripObject)
    #print("Flight is", newTrip.initFlight[-1].timeEnd)
    #print("Return flight is", newTrip.finFlight[0].timeStart)
    days = newTrip.days
    
    for day in days:
        
        if (day != None):
            
            print("Day starting date is:", day.timeStart)
            
            if (len(day.activities) > 0):
                
                hotelCoords = day.placeOfStay.destination.split(',')
                day.transport = []
                firstActivityCoords = day.activities[0].destination.split(',')
                startTime = day.timeStart
                print("This is starTime", startTime)
                hotelToFirst = transportObject.getTransportByTime(hotelCoords[0], hotelCoords[1], firstActivityCoords[0], firstActivityCoords[1], str(startTime.isoformat()))
                startTime = hotelToFirst[-1].timeEnd
                startTime = startTime + datetime.timedelta(minutes=5)
                day.activities[0].timeStart = startTime
                endTime = startTime + datetime.timedelta(hours=3)
                day.activities[0].timeEnd = endTime
                currTime = endTime + datetime.timedelta(minutes=60)
                currCoords = day.activities[0].destination.split(',')
                day.transport.append(hotelToFirst)
                print("First activity is ", day.activities[0])
                
                for activity in day.activities[1:]:
                    
                    print("current activity is", activity)
                    nextActivityCoords = activity.destination.split(',')
                    transportToActivity = transportObject.getTransportByTime(currCoords[0], currCoords[1], nextActivityCoords[0], nextActivityCoords[1], str(currTime.isoformat()))
                    currTime = transportToActivity[-1].timeEnd
                    currTime = currTime + datetime.timedelta(minutes=5)
                    activity.timeStart = currTime
                    currTime = currTime + datetime.timedelta(hours=3)
                    activity.timeEnd = currTime
                    currTime = currTime + datetime.timedelta(minutes=60)
                    currCoords = nextActivityCoords
                    day.transport.append(transportToActivity)
                    
                lastToHotel = transportObject.getTransportByTime(currCoords[0], currCoords[1], hotelCoords[0], hotelCoords[1], str(currTime.isoformat()))
                
                day.transport.append(lastToHotel)
                
    return newTrip