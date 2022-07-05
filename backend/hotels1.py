# Install the Python library from https://pypi.org/project/amadeus
from datetime import datetime
from amadeus import Client, ResponseError
import sys
import importlib
import json


import sys
import os


import classes
class hotelFunctions:
    def __init__(self, amadeus):
        self.amadeus = amadeus
    def getHotels(self, city, adult):
        try:
            # Get list of Hotels by city code
            hotels_by_city = self.amadeus.shopping.hotel_offers.get(cityCode=city,adults=adult)

            offers = []
            # create list of hotels
            for hotel in hotels_by_city.data:
                url = hotel["hotel"]["media"][0]['uri']
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
            Returns activities for a location geolocation coordinates
            '''
            response = self.amadeus.shopping.activities.get(latitude = latitude, longitude = longitude)


            # create list of activities
            activities = []
            for activity in response.data:

                try:
                    title = activity['name']

                    try:  
                        cost = float(activity['price']['amount'])
                    except:
                        cost = 0

                    try:
                        url = activity['bookingLink']
                    except:
                        url = "/404/"

                    dest = str(activity["geoCode"]["latitude"]) + "," + str(activity["geoCode"]["longitude"])

                    try:
                        photos = activity['pictures']
                    except:
                        photos = "/404/"
                    act = classes.Activity(3, cost, None, None, title, url, photos, True, dest)
                    activities.append(act)
                except:
                    continue


            return activities
        except ResponseError as error:
            # print(error)
            return []
        except:
            return activities


    def getHotelsByGeocode(self, latitude, longitude):
        try:
            date = datetime.strptime("2022-11-01", '%Y-%m-%d')
            # Get list of Hotels by city code
            hotels_by_city = self.amadeus.reference_data.locations.hotels.by_geocode.get(longitude=longitude,latitude=latitude)

            offers = []
            for hotelID in hotels_by_city.data:

                id = hotelID["hotelId"]

                # get details about the hotel
                hotel = self.getHotelByID(id)

                if (type(hotel) is list):
                    continue

                try:
                    url = hotel["hotel"]["media"][0]['uri']
                except:
                    url = "/404/"


                price = hotel["offers"][0]["price"]["total"]
                price = float(price)

                checkIn = hotel["offers"][0]["checkInDate"]
                checkOut = hotel["offers"][0]["checkOutDate"]

                title = hotel["hotel"]["name"]

                hotelLatitude = hotel["hotel"]["latitude"]
                hotelLongitude = hotel["hotel"]["longitude"]
                city = str(hotelLatitude) + "," + str(hotelLongitude)
                hotel = classes.PlaceOfStay(None, price, checkIn, checkOut, title, url, None, True, city)

                offers.append(hotel)

                if (len(offers) > 0):
                    break

            return offers
        except ResponseError as error:
            print("ERROR IS: ", error)
            return []
        except Exception as E:
            print("Those are it:", E)
            return offers



    def getHotelByID(self, hotelID):
        try:
            # Get hotel by id
            hotel = self.amadeus.shopping.hotel_offers_search.get(hotelIds=hotelID)

            if (type(hotel.data) is list and len(hotel.data) > 0):
                return hotel.data[0]

            return hotel.data
        except ResponseError as error:
            print("cant find hotel by id", error)
            return []



# testing
if __name__ == '__main__':

    amadeus = Client(
        client_id='CGwOmHn7cmfAIuUcbqUiaPC5LAyAvwAG',
        client_secret='rKvILHDsjxcCh6yq'
        )


    x = hotelFunctions(amadeus)
    # act = x.getActivities(40.761794, -73.972670,0)
    # print(act)

    # hotel = x.getHotelsByGeocode(32.080691, 34.779109)
    # print(hotel)
    
