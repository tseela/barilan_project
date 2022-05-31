from amadeus import Client, ResponseError

amadeus = Client(
    client_id='CGwOmHn7cmfAIuUcbqUiaPC5LAyAvwAG',
    client_secret='rKvILHDsjxcCh6yq'
)

try:
    response = amadeus.shopping.flight_offers_search.get(
        originLocationCode='MAD',
        destinationLocationCode='ATH',
        departureDate='2022-11-01',
        adults=1)
    print(response.data)
    print(len(response.data))
    print(response.data[1])
except ResponseError as error:
    print(error)