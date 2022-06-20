import classes
import datetime
class Flights:
    def __init__(self, amadeus_client):
        self.amadeus = amadeus_client
    
    def getFlightObjects(self, srcAirportCode, dstAirportCode, date, passengersCount):
        response = self.amadeus.shopping.flight_offers_search.get(
        originLocationCode=srcAirportCode,
        destinationLocationCode=dstAirportCode,
        departureDate=date,
        adults=passengersCount).data
        parsedData = self.parseFlightResponse(response)
        return parsedData
    
    def extractDuration(self, itineraries):
        hour = 0
        minute = 0
        for i in itineraries:
            i = {x.replace(' ', ''): v
    for x, v in i.items()}
            currDur = i['duration'].split('M')
            if (len(currDur) == 1):
                hour += int(currDur[-1].split('PT')[-1].split('H')[0])
            if (len(currDur) == 2):
                minute += int(currDur[0].split('H')[-1])
                hour += int(currDur[0].split('H')[0].split('PT')[-1])
        return hour + minute / 60
    
    def extractPrice(self, price):
        price = {x.replace(' ', ''): v
             for x, v in price.items()}
        return price['total']
    
    def extractItinerary(self, itineraries):
        flightList = []
        for i in itineraries[0]['segments']:
            print(i)
            timeStart = datetime.datetime.strptime(i['departure']['at'], '%Y-%d-%mT%H:%M:%S')
            timeEnd = datetime.datetime.strptime(i['arrival']['at'], '%Y-%d-%mT%H:%M:%S')
            title = i['carrierCode'] + i['number'] # flight number
            duration = i['duration']
            orderInAdvance = True
            try:
                terminal = i['departure']['terminal']
            except:
                print("No terminal in answer")
                terminal = str(1)
            originAirport = i['departure']['iataCode']
            placeOfOrigin = originAirport + '-' + terminal
            destination = i['arrival']['iataCode']
            methodOfTransport = Transportation.FLIGHT
            cost = 0
            duration = int((timeEnd - timeStart).total_seconds()) / 3600
            currTransportObject = Transport(duration, cost, timeStart, timeEnd, title, "", "", orderInAdvance, "", methodOfTransport, "", placeOfOrigin, destination) # consider adding coordinates.
            flightList.append(currTransportObject)
        return flightList
    def flightEndingTimeArray(self, response):
        resArr = []
        for i in response['itineraries'][0]['segments']:
            resArr.append(i['arrival']['at'])
        return resArr
    
    def flightDestinationLocationArray(self, response):
        resArr = []
        for i in response['itineraries'][0]['segments']:
            resArr.append({'airport' : i['arrival']['iataCode'],  'terminal' : i['arrival']['terminal']})
        return resArr
    
    def flightStartingTimeArray(self, response):
        resArr = []
        for i in response['itineraries'][0]['segments']:
            resArr.append(i['departure']['at'])
        return resArr
    
    def flightSourceLocationArray(self, response):
        resArr = []
        for i in response['itineraries'][0]['segments']:
            resArr.append({'airport' : i['departure']['iataCode'], 'tיerminal' : i['departure']['terminal']})
        return resArr
    
    def parseFlightResponse(self, response):
        resultArr = []
        for option in response:
            currResultDict = {}
            option = {x.replace(' ', ''): v
     for x, v in option.items()}
#             currResultDict['duration'] = self.extractDuration(option['itineraries'])
            price = self.extractPrice(option['price'])
            currResultDict['itinerary'] = self.extractItinerary(option['itineraries'])
#             currResultDict['timeStart'] = self.flightStartingTimeArray(option)
#             currResultDict['timeEnd'] = self.flightEndingTimeArray(option)
            itineraryList = self.extractItinerary(option['itineraries'])
            if (len(itineraryList) > 0):
                itineraryList[0].cost = price
            resultArr.append(itineraryList)
        if (len(resultArr) > 0):
            return resultArr[-1]
        return resultArr