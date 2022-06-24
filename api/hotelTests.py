from amadeus import Client, ResponseError



if __name__ == '__main__':
    amadeus = Client(
        client_id='CGwOmHn7cmfAIuUcbqUiaPC5LAyAvwAG',
        client_secret='rKvILHDsjxcCh6yq'
    )

    try:
        # Get list of Hotels by city code
        # hotels_by_city = amadeus.shopping.hotel_offers.get(cityCode=city,adults=adult)
        hotels_by_city = amadeus.reference_data.locations.hotels.by_geocode.get(latitude=32.079664,longitude=34.767410)

        print(hotels_by_city.data)
        print(len(hotels_by_city.data))
        print(hotels_by_city.data[0])
    except ResponseError as error:
        raise error

    x = amadeus.reference_data.locations.hotels.by_hotels.get(hotelIds='INTLVA83')
    print(x.data)
    y = amadeus.shopping.hotel_offers.get(hotelIds='RTPAR001')
    print(y.data[0])
    print(y.data[0])

