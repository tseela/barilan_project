from html import entities
from amadeus import Client, ResponseError, Location
import amadeus


import requests
import ast
import json
# amadeus = Client(
#     client_id='CGwOmHn7cmfAIuUcbqUiaPC5LAyAvwAG',
#     client_secret='rKvILHDsjxcCh6yq'
# )


# try:
#     response = amadeus.shopping.flight_offers_search.get(
#         originLocationCode='MAD',
#         destinationLocationCode='ATH',
#         departureDate='2022-11-01',
#         adults=1)
#     print(response.data)


# except ResponseError as error:
#     print(error)

# try:
#     # Get list of Hotels by city code
#     hotels_by_city = amadeus.shopping.hotel_offers_search.get(
#         hotelIds='RTPAR001', adults='2')
#     print(hotels_by_city.data)
# except ResponseError as error:
#     print(error)

# try:
#     response = amadeus.reference_data.locations.get(keyword='BOS', subType=Location.ANY)
#     print(response.data)
# except ResponseError as error:
#     print(error)

# returns the ids of destination
def findDestination(query ,currency, locale):
    url = "https://hotels-com-provider.p.rapidapi.com/v1/destinations/search"

    querystring = {"query":"Tel Aviv","currency":"ILS","locale":"iw_IL"}

    headers = {
	    "X-RapidAPI-Host": "hotels-com-provider.p.rapidapi.com",
	    "X-RapidAPI-Key": "af86b777efmsh69435b8ba6e17cep126b88jsna15b99d4f1d0"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    city = json.loads(response.text)
    # print(city["suggestions"])
    entities = 0
    for w in city["suggestions"]:
        if(w['group'] == 'CITY_GROUP'):
            entities = w['entities']
            break
    if(entities == 0):
        return []
     
    ids = []
    for entity in entities:
        ids.append(entity["destinationId"])
    return ids

def findHotelByID(id):
    import requests

    url = "https://hotels-com-provider.p.rapidapi.com/v1/hotels/search"

    querystring = {"checkin_date":"2022-06-26",
        "checkout_date":"2022-06-27",
        "sort_order":"STAR_RATING_HIGHEST_FIRST",
        "destination_id":id,
        "adults_number":"1",
        "locale":"en_US",
        "currency":"USD",
        "children_ages":"4,0,15",
        "price_min":"10",
        "star_rating_ids":"3,4,5",
        "accommodation_ids":"20,8,15,5,1",
        "price_max":"500",
        "page_number":"1",
        "theme_ids":"14,27,25",
        "amenity_ids":"527,2063",
        "guest_rating_min":"4"}

    headers = {
        "X-RapidAPI-Host": "hotels-com-provider.p.rapidapi.com",
        "X-RapidAPI-Key": "af86b777efmsh69435b8ba6e17cep126b88jsna15b99d4f1d0"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    print(response.text)
    return response.text

# url = "https://hotels-com-provider.p.rapidapi.com/v1/destinations/search"

# querystring = {"query":"London","currency":"USD","locale":"en_US"}

# headers = {
# 	"X-RapidAPI-Host": "hotels-com-provider.p.rapidapi.com",
# 	"X-RapidAPI-Key": "af86b777efmsh69435b8ba6e17cep126b88jsna15b99d4f1d0"
# }

# response = requests.request("GET", url, headers=headers, params=querystring)

# print(response.text)

# url = "https://hotels-com-provider.p.rapidapi.com/v1/destinations/search"

# querystring = {"query":"Tel Aviv","currency":"ILS","locale":"iw_IL"}

# headers = {
# 	"X-RapidAPI-Host": "hotels-com-provider.p.rapidapi.com",
# 	"X-RapidAPI-Key": "af86b777efmsh69435b8ba6e17cep126b88jsna15b99d4f1d0"
# }

# response = requests.request("GET", url, headers=headers, params=querystring)

# print(response.text)

# print(json.loads(response.text)['query'])
# x = json.loads(response.text)
# for y in x:
#     print(y)
#     # print(x[y])
# print(len(x['suggestions']))
# for y in x['suggestions']:
#     print(y)




# url = "https://hotels-com-provider.p.rapidapi.com/v1/hotels/search"

# querystring = {"checkin_date":"2022-06-26","checkout_date":"2022-06-27","sort_order":"STAR_RATING_HIGHEST_FIRST","destination_id":"1708350","adults_number":"1","locale":"en_US","currency":"USD","children_ages":"4,0,15","price_min":"10","star_rating_ids":"3,4,5","accommodation_ids":"20,8,15,5,1","price_max":"500","page_number":"1","theme_ids":"14,27,25","amenity_ids":"527,2063","guest_rating_min":"4"}

# headers = {
# 	"X-RapidAPI-Host": "hotels-com-provider.p.rapidapi.com",
# 	"X-RapidAPI-Key": "af86b777efmsh69435b8ba6e17cep126b88jsna15b99d4f1d0"
# }

# response = requests.request("GET", url, headers=headers, params=querystring)

# print(response.text)


z = findDestination("Tel Aviv","ILS","iw_IL")
print(z)
hotel = json.loads(findHotelByID(z[0]))
print(type(hotel))
for d in hotel:
    print(d)