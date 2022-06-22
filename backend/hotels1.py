# Install the Python library from https://pypi.org/project/amadeus
from datetime import datetime
from amadeus import Client, ResponseError
import sys
import importlib
import json


# from ..objects import classes
# t = classes.Trip(1,2,3,4,5,6)

import sys
import os
# print('/'.join(os.getcwd().split('/')[:-1]))
# sys.path.append('/'.join(os.getcwd().split('/')[:-1]))
# from algo.libs.classes import *



import classes
class hotelFunctions:
    def __init__(self, amadeus):
        self.amadeus = amadeus
    def getHotels(self, city, adult):
        try:
            # Get list of Hotels by city code
            hotels_by_city = self.amadeus.shopping.hotel_offers.get(cityCode=city,adults=adult)

            offers = []
            for hotel in hotels_by_city.data:
                url = hotel["hotel"]["media"][0]['uri']
                # print(hotel["offers"][0]["price"])
                price = hotel["offers"][0]["price"]["total"]
                price = float(price)

                checkIn = hotel["offers"][0]["checkInDate"]
                checkOut = hotel["offers"][0]["checkOutDate"]

                title = hotel["hotel"]["name"]
                hotel = classes.PlaceOfStay(None, price, checkIn, checkOut, title, url, None, True, city)
                # print (hotel.__dict__)
                offers.append(hotel)

            return offers
        except ResponseError as error:
            # raise error
            print("ERROR IS: ", error)
            return []
        except Exception as E:
            print("Those are it:", E)
            return offers



    def getActivities(self, latitude, longitude, radius):
        try:
            '''
            Returns activities for a location in Barcelona based on geolocation coordinates
            '''
            response = self.amadeus.shopping.activities.get(latitude = latitude, longitude = longitude)

            #print(json.dumps(response.data, sort_keys=False, indent=4))

            activities = []
            for activity in response.data:
                title = activity['name']
                cost = float(activity['price']['amount'])
                url = activity['bookingLink']
                photos = activity['pictures']
                dest = activity["geoCode"]["latitude"] + "," + activity["geoCode"]["longitude"]

                act = classes.Activity(None, cost, None, None, title, url, photos, True, dest)
                #print(act.__dict__)
                activities.append(act)

            # print(response.data)
            return activities
        except ResponseError as error:
            # raise error
            return []
        except:
            return activities


    def getHotelsByGeocode(self, latitude, longitude):
        try:
            date = datetime.strptime("2022-11-01", '%Y-%m-%d')
            # Get list of Hotels by city code
            hotels_by_city = self.amadeus.reference_data.locations.hotels.by_geocode.get(longitude=longitude,latitude=latitude)
            # print(hotels_by_city.data)
            offers = []
            for hotelID in hotels_by_city.data:
                # print(hotelID)
                id = hotelID["hotelId"]
                # print(id)
                hotel = self.getHotelByID(id)

                if (type(hotel) is list):
                    continue
                
                try:
                    url = hotel["hotel"]["media"][0]['uri']
                except:
                    if (len(offers) == 0):
                        continue
                    else:
                        return offers
                # print(hotel["offers"][0]["price"])
                price = hotel["offers"][0]["price"]["total"]
                price = float(price)

                checkIn = hotel["offers"][0]["checkInDate"]
                checkOut = hotel["offers"][0]["checkOutDate"]

                title = hotel["hotel"]["name"]

                hotelLatitude = hotel["hotel"]["latitude"]
                hotelLongitude = hotel["hotel"]["longitude"]
                city = str(hotelLatitude) + "," + str(hotelLongitude)
                hotel = classes.PlaceOfStay(None, price, checkIn, checkOut, title, url, None, True, city)
                # print (hotel.__dict__)
                offers.append(hotel)

            return offers
        except ResponseError as error:
            # raise error
            print("ERROR IS: ", error)
            return []
        except Exception as E:
            print("Those are it:", E)
            return offers



    def getHotelByID(self, hotelID):
        try:
            # Get list of Hotels by city code
            date = datetime.strptime("2022-11-01", '%Y-%m-%d')
            date2 = datetime.strptime("2022-11-08", '%Y-%m-%d')
            # hotel = self.amadeus.shopping.hotel_offers.get(hotelIds=hotelID, checkInDate =date, checkOutDate = date2)

            # hotel = self.amadeus.shopping.hotel_offers.get(hotelIds=hotelID)
            # hotel = amadeus.reference_data.locations.hotels.by_hotels.get(hotelIds=hotelID)

            hotel = amadeus.shopping.hotel_offers_search.get(hotelIds=hotelID)

            # print(hotel.data)
            if (type(hotel.data) is list and len(hotel.data) > 0):
                return hotel.data[0]

            return hotel.data
        except ResponseError as error:
            print("cant find hotel by id", error)
            # raise error
            return []


# maybe use to get another activities
# def getActivities2(latitude, longitude, radius):
#     try:
#         response = amadeus.reference_data.locations.points_of_interest.get(latitude=latitude, longitude=longitude)
#         print(json.dumps(response.data, sort_keys=False, indent=4))
#         # print(response.data)

#     except ResponseError as error:
#         raise error



if __name__ == '__main__':
    amadeus = Client(
        client_id='CGwOmHn7cmfAIuUcbqUiaPC5LAyAvwAG',
        client_secret='rKvILHDsjxcCh6yq',
        log_level='debug'
    )

    amadeus = Client(
        client_id='3Hjzstks6Ahiptx9IFmkJhnbMuXMErgM',
        client_secret='Ol5zYr6FEIAGGDsG' 
    )
    # this is ron


    # hotels = getHotels('TLV',2)
    # print(hotels)


    # res = getActivities(32.079664, 34.767410, 0)
    # print(res)
    # print(res[0])
    # print(res[0]['price'])


    # x = getHotelByID('BWTLV023')
    # print(x)
    # date = datetime.strptime("2022-11-01", '%Y-%m-%d')
    # print(str(date)[:9])
    x = hotelFunctions(amadeus)

    # hotels = x.getHotelsByGeocode(30.044770, 31.242940)
    # print(hotels)
    # hotels = x.getHotelsByGeocode(32.079664, 34.767410)

    
    # print(hotels)
    hotels = x.getHotelsByGeocode(51.506412, -0.139257)
    print(hotels)

    hotels = x.getHotelsByGeocode(40.761794, -73.972670)
    print(hotels)


    # hotels = x.getHotels("TLV", 2)

