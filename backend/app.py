# from flask import Flask
# import pymongo
# from crypt import methods
from typing import List
from flask import Flask , request, jsonify,make_response, render_template, session
import jwt
from datetime import datetime, timedelta
from functools import wraps

import pymongo
from flask_bcrypt import bcrypt
# import sys

# from classes import Activity, Day
# sys.path.append('../algo/libs/classes.py')
import classes
from bson import ObjectId
import json
import tripAlgo
import csv

import traceback


# server
app = Flask(__name__)
app.config['SECRET_KEY'] = '03a5t89c1pf9Uc0a0f7E'


# db
client = pymongo.MongoClient("mongodb+srv://TripDesigner:ShakedKing@tripdesigner.i9pia.mongodb.net/?retryWrites=true&w=majority")
db = client.test
db = client.tripDesigner
users = db.Users
trips = db.Trips

# days = db.Days
# activities = db.Activities
# transportations = db.Transport
# placeOfStay = db.PlaceOfStay

# maps of airports and cities for frontend to use
_airportsMap = []
_countriesMap = []
_regionsMap = []
_citiesMap = []

with open('metadata/worldcities.csv', encoding="utf-8") as f:
    _citiesMap = [{k: v for k, v in row.items()}
        for row in csv.DictReader(f, skipinitialspace=True)]

with open('metadata/regions.csv', encoding="utf-8") as f:
    _regionsMap = [{k: v for k, v in row.items()}
        for row in csv.DictReader(f, skipinitialspace=True)]

with open('metadata/countries.csv', encoding="utf-8") as f:
    _countriesMap = [{k: v for k, v in row.items()}
        for row in csv.DictReader(f, skipinitialspace=True)]

headers = [ 'name', 'latitude_deg', 'longitude_deg', 'iso_region', 'municipality', 'iso_country', 'iata_code' ]
with open('metadata/airports.csv', encoding="utf-8") as f:
    _airportsMap = [{k: v for k, v in row.items() if k in headers}
        for row in csv.DictReader(f, skipinitialspace=True)]



#Token check
def token_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        token = request.json['token']
        if not token:
            return jsonify({'Alert!' : 'Token is missing!'}), 405
        try:
            payload = jwt.decode(token['secret'], app.config['SECRET_KEY'], algorithms="HS256")
            if payload['user'] != token['user']:
                raise Exception("Decoded username doesn't match the encoded one.")
            return func(*args, **kwargs)
        except Exception as inst:
            return jsonify({'Alert!' : 'Invalid Token!'}), 405
    return decorated

# get airpots
@app.route('/getAirportsAndDistrictsLists', methods=['GET'])
def getAirportsAndDistrictsLists():
    return jsonify({ 'airportsMap' : _airportsMap, 'countriesMap' : _countriesMap, 'regionsMap' : _regionsMap, 'citiesMap' : _citiesMap }), 200



# sign up
# @return status
@app.route('/signup', methods=['POST'])
def signup():
    return signUp(request.json['username'], request.json['password'])


def signUp(username, password):
    if users.find_one({"username":username}) != None:
        return jsonify({'status': "fail", "message":"Cannot assingn this username"}), 401

    # salt is for password
    salt = bcrypt.gensalt()
    user = {
        "username" : username,
        "password" : bcrypt.hashpw((password + salt.decode()).encode(), bcrypt.gensalt()),
        "salt" : salt,
        "trips" : []
    }
    users.insert_one(user)
    return jsonify({'status': "successful", "message": "User created successfuly"}), 200



# sign in
# @return status
@app.route('/signin', methods=['POST'])
def signin():
    return signIn(request.json['username'], request.json['password'])


def signIn(username, password):
    user = users.find_one({"username":username})
    # return bcrypt.checkpw((password + user['salt'].decode()).encode() , user['password'])

    # check the password
    if user == None or not bcrypt.checkpw((password + user['salt'].decode()).encode() , user['password']):
        return make_response("Username not found or wrong password", 403, {'WWW-Authentic' : 'Basic realm:"Authentcation faild!'})

    session['logged_in'] = True

    # the token
    token = {
        'user' : username,
        'secret' : jwt.encode({'pass' : password, 'user' : username,
                'expiration' : str(datetime.utcnow() + timedelta(seconds=120))}, app.config['SECRET_KEY'], algorithm="HS256")
    }

    return jsonify({'token' : token}), 200


@app.route('/createTrip', methods=['POST'])
# @return tripID
def createTrip():

    flags = request.json['flags']
    trip = tripAlgo.getTrip(request.json['srcAirport'], request.json['startDate'], request.json['duration'], request.json['numOfPeople'], flags['isFastPaced'], flags['isMuseumOriented'], flags['isLuxuriance'], flags['isLowCost'], request.json['destination'])
    tripJSON = TripToJson(trip)

    return tripJSON, 200



@app.route("/insertTripToUser", methods=['POST'])
@token_required
def insertTripToUser():
    try:
        trip = request.json["trip"]

        # find user
        user = users.find_one({"username" : request.json["token"]["user"]})
        

        trip["userId"] = ObjectId(user["_id"])

        user["_id"] = ObjectId(user["_id"])
        # insert trip to db
        tripID = trips.insert_one(trip).inserted_id


        addTripToUser(request.json["token"]["user"], tripID)
        return str(tripID) , 200
    except:
        return "Cannot insert trip", 403



@app.route('/getTrip', methods=['POST'])
@token_required
def GetTrip():
    try:
        # find trip
        trip = trips.find_one({'_id': ObjectId(request.json['tripID'])})

        trip['_id'] = str(trip['_id'])
        trip['userId'] = str(trip['userId'])
        return trip, 200
    except:
        return "Cant get trip", 403
    
def getTripById(id):
    try:
        trip = trips.find_one({'_id': ObjectId(id)})

        trip['_id'] = str(trip['_id'])
        trip['userId'] = str(trip['userId'])
        return trip
    except:
        return {}


@app.route('/updateTrip', methods=['POST'])
@token_required
def UpdateTrip():
    try:
        return updateTrip(request.json['trip']['_id'], request.json['trip']), 200
    except:
        print(print(traceback.format_exc()))
        return "Cant update trip", 403


def updateTrip(tripId, newTrip):
    newTrip = json.loads(editTrip(newTrip))
    newTrip['_id'] = ObjectId(tripId)
    newTrip['userId'] = ObjectId(newTrip['userId'])

    tripId = ObjectId(tripId)

    ret = trips.find_one_and_update({'_id':(tripId)}, {'$set':newTrip})

    return "updated"




@app.route('/getTripsByUser')
@token_required
def GetTripsByUser():
    try:
        return getTripsByusername(request.json['username']), 200
    except:
        return "Cant get trips", 403



@app.route('/getTripsAndNamesByUser', methods=['POST'])
@token_required
def getTripsAndNamesByUser():
    try:
        username = request.json['username']
        user = users.find_one({"username" : username})
        trips = []
        if (user['trips'] == None):
            return jsonify([]), 200

        # for every trip in user's trips get the trip object
        for trip in user['trips']:
            name = getTripById(trip)['name']
            trips.append({'id':str(trip), 'name':name})
        return jsonify(trips), 200
    except:
        return "Cant get trips", 403



# @return trips objects
def getTripsByusername(name):
    user = users.find_one({"username" : name})

    trips = []
    if (user['trips'] == None):
        return trips

    for trip in user['trips']:
        trips.append(getTripById(trip))

    return trips


@app.route('/addTripToUser', methods=['POST'])
@token_required
def AddTripToUser():
    try:
        return addTripToUser(request.json['username'], request.json['tripID']), 200
    except:
        return "Cant add trips", 403


# add the id of trip to user
def addTripToUser(name, tripID):
    user = users.find_one({"username" : name})
    
    # if user doesn't have any trips
    if (not type(user['trips']) == list):
        user['trips'] = [tripID]

    # else add the trip to the list
    else:
        if (tripID in user['trips']):
            return
        user['trips'] = user['trips'] + [ObjectId(tripID)]

    user = users.find_one_and_update({"username" : name}, update={ "$set": {"trips" : user['trips']}})




@app.route('/removeTripFromUser', methods=['POST'])
@token_required
def RemoveTripFromUser():
    try:
        return removeTripfromUser(request.json['user'], request.json['id']), 200
    except:
        return "Cant romve trip", 403


def removeTripfromUser(name, tripID):
    tripID = ObjectId(tripID)
    user = users.find_one({"username" : name})

    # if there is no trips
    if (not type(user['trips']) == list):
        return "trip not in user"

    else:
        if (tripID not in user['trips']):
            return "trip not in user"
        user['trips'].remove(tripID)

    user = users.find_one_and_update({"username" : name}, update={ "$set": {"trips" : user['trips']}})
    return "deleted trip from user"



@app.route('/createTripAndAdd', methods=['POST'])
@token_required
def CreateTripAndAdd():
    try:
        return createTripAndAdd(request.json['username']), 200
    except:
        return "Cant create and insert", 403

def createTripAndAdd(name):
    id = createTrip()
    addTripToUser(name,id)


def editTrip(jsonTrip):
    trip = JsonToTrip(jsonTrip)
    trip = tripAlgo.switchingTripActivities(trip)
    trip = TripToJson(trip)
    return trip


# @app.route('/changePassword', methods=['POST'])
# def changepassword():
#     return changePassword(request.json['username'], request.json['password'], request.json['newPassword'])

 
# def changePassword(username, password, newPassword):
#     user = users.find_one({"username":username})
#     if user == None:
#         return "Username not found"
#     if user["password"] != password:
#         return "Wrong password"
#     if password == newPassword:
#         return "New password cannot be equals to old password"
#     users.find_one_and_update({"username":username}, update={ "$set": {"password":newPassword}})
#     return "ok"

# @app.route('/changeUsername', methods=['POST'])
# def changeusername():
#     return changeUsername(request.json['username'], request.json['password'], request.json['newUsername'])


# def changeUsername(username, password, newUsername):
#     user = users.find_one({"username":username})
#     if user == None:
#         return "Username not found"
#     if user["password"] != password:
#         return "Wrong password"
#     if username == newUsername:
#         return "New username cannot be equals to old username"
#     users.find_one_and_update({"username":username}, update={ "$set": {"username":newUsername}})
#     return "ok"



# trip object to json
def TripToJson(trip):
    transOptions = {0 : "NONE", 1 : "BUS", 2 : "TRAIN", 3 : "RAM", 4 : "PUBLICTAXI", 5 : "FLIGHT"}


    newDays = []
    trip.endDate = str(trip.endDate)
    trip.startDate = str(trip.startDate)

    # turns every day object to json
    for day in trip.days:
        if day is None:
            print('none')
            continue

        day.timeStart = str(day.timeStart)
        day.timeEnd = str(day.timeEnd)
        



        newacts = []
        for act in day.activities:

            act.timeStart = str(act.timeStart)
            act.timeEnd = str(act.timeEnd)

            actson = act.__dict__
            newacts.append(actson)
        day.activities = newacts




        newtrans = []
        for trans in day.transportation:
            subtrans = []
            for trn in trans:
                trn.timeStart = str(trn.timeStart)
                trn.timeEnd = str(trn.timeEnd)
                trn.duration = str(trn.duration)


                transon = trn.__dict__
                transon["methodOfTransportation"] = transOptions[int(transon["methodOfTransportation"])]


                subtrans.append(transon)
            newtrans.append(subtrans)
        day.transportation = newtrans




        day.placeOfStay.timeStart = str(day.placeOfStay.timeStart)
        day.placeOfStay.timeEnd = str(day.placeOfStay.timeEnd)
        day.placeOfStay = day.placeOfStay.__dict__

        newDays.append(day.__dict__)



    trip.days = newDays



    trip.userId = str(trip.__dict__["userId"])



    newFlights = []
    for flight in trip.initFlight:

        flight.timeStart = str(flight.timeStart)
        flight.timeEnd = str(flight.timeEnd)

        nFlight = flight.__dict__
        nFlight["methodOfTransportation"] = transOptions.get(int(nFlight["methodOfTransportation"]))
        newFlights.append(nFlight)
    trip.initFlight = newFlights




    newflights2 = []
    for flight in trip.finFlight:

        flight.timeStart = str(flight.timeStart)
        flight.timeEnd = str(flight.timeEnd)

        nFlight = flight.__dict__
        nFlight["methodOfTransportation"] = transOptions.get(int(nFlight["methodOfTransportation"]))
        newflights2.append(nFlight)
    trip.finFlight = newflights2



    return json.dumps(trip.__dict__)




# turns json to trip object
def JsonToTrip(jsonTrip):
    transOptions = { "NONE" : 0, "BUS" : 1, "TRAIN" : 2, "RAM" : 3, "PUBLICTAXI" : 4, "FLIGHT" : 5}

    trip = jsonTrip

    newDays = []
    trip['startDate'] = datetime.strptime(trip['startDate'].replace(" ", "T"), '%Y-%m-%dT%H:%M:%S')
    trip['endDate'] = datetime.strptime(trip['endDate'].replace(" ", "T"), '%Y-%m-%dT%H:%M:%S')



    for day in trip['days']:
        day['timeStart'] = datetime.strptime(day['timeStart'].replace(" ", "T"), '%Y-%m-%dT%H:%M:%S')
        day['timeEnd'] = datetime.strptime(day['timeEnd'].replace(" ", "T"), '%Y-%m-%dT%H:%M:%S')




        newacts = []
        for act in day['activities']:
            act['timeStart'] = datetime.strptime(act['timeStart'].replace(" ", "T"), '%Y-%m-%dT%H:%M:%S')
            act['timeEnd'] = datetime.strptime(act['timeEnd'].replace(" ", "T"), '%Y-%m-%dT%H:%M:%S')

            actson = classes.Activity.DictToActivity(act)
            newacts.append(actson)
        day['activities'] = newacts





        newtrans = []
        for trans in day["transportation"]:
            subtrans = []
            for trn in trans:
                trn['timeStart'] = datetime.strptime(trn['timeStart'].replace(" ", "T"), '%Y-%m-%dT%H:%M:%S')
                trn['timeEnd'] = datetime.strptime(trn['timeEnd'].replace(" ", "T"), '%Y-%m-%dT%H:%M:%S')
                transon = classes.Transport.DictToTransport(trn)
                transon.methodOfTransportation = transOptions[transon.methodOfTransportation]

                subtrans.append(transon)
            newtrans.append(subtrans)

        day["transportation"] = newtrans





        day["placeOfStay"]["timeStart"] = datetime.strptime(day["placeOfStay"]["timeStart"].split(" ")[0], '%Y-%m-%d')
        day["placeOfStay"]["timeEnd"] = datetime.strptime(day["placeOfStay"]["timeEnd"].split(" ")[0], '%Y-%m-%d')
        day["placeOfStay"] = classes.PlaceOfStay.DictToPlace(day["placeOfStay"])
        newday = classes.Day.DictToDay(day)
        newDays.append(newday)




    trip['days'] = newDays
    trip['userId'] = ObjectId(trip['userId'])




    newFlights = []
    for flight in trip["initFlight"]:
                
        flight['timeStart'] = datetime.strptime(flight['timeStart'].replace(" ", "T"), '%Y-%m-%dT%H:%M:%S')
        flight['timeEnd'] = datetime.strptime(flight['timeEnd'].replace(" ", "T"), '%Y-%m-%dT%H:%M:%S')
        

        flight["methodOfTransportation"] = transOptions[flight["methodOfTransportation"]]
        newFlights.append(classes.Transport.DictToTransport(flight))
        
    trip["initFlight"] = newFlights





    newFlights2 = []
    for flight in trip["finFlight"]:
        
        flight['timeStart'] = datetime.strptime(flight['timeStart'].replace(" ", "T"), '%Y-%m-%dT%H:%M:%S')
        flight['timeEnd'] = datetime.strptime(flight['timeEnd'].replace(" ", "T"), '%Y-%m-%dT%H:%M:%S')

        flight["methodOfTransportation"] = transOptions[flight["methodOfTransportation"]]
        newFlights2.append(classes.Transport.DictToTransport(flight))
    trip["finFlight"] = newFlights2



    x = classes.Trip.DictToTrip(trip)
    return classes.Trip.DictToTrip(trip)


if __name__ == '__main__':
    app.run(debug=True)

