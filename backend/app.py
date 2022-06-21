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



# server
app = Flask(__name__)
app.config['SECRET_KEY'] = '03a5t89c1pf9Uc0a0f7E'
# db
# client = pymongo.MongoClient("mongodb+srv://TripDesigner:ShakedKing@tripdesigner.i9pia.mongodb.net/Users?retryWrites=true&w=majority", connect=False)

client = pymongo.MongoClient("mongodb+srv://TripDesigner:ShakedKing@tripdesigner.i9pia.mongodb.net/?retryWrites=true&w=majority")
db = client.test
# client = pymongo.MongoClient("https://data.mongodb-api.com/app/data-xwflj/endpoint/data/beta")
db = client.tripDesigner
users = db.Users
trips = db.Trips

days = db.Days
activities = db.Activities
transportations = db.Transport
placeOfStay = db.PlaceOfStay

# maps of airports and cities for frontend to use
_airportsMap = []
_countriesMap = []
_regionsMap = []

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

# example
@app.route('/api', methods=[ 'POST'])
def example():
    return {
        'name': 'ola amigos'
    }


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


@app.route('/getAirportsAndDistrictsLists', methods=['GET'])
def getAirportsAndDistrictsLists():
    print(_regionsMap[0])
    return jsonify({ 'airportsMap' : _airportsMap, 'countriesMap' : _countriesMap, 'regionsMap' : _regionsMap }), 200


# acttualy the 'then' statements need to be what Tseela want.
@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('homePage.html')
    else:
        return render_template('trips.html')



@app.route('/trips')
def Trips():
    return render_template('trips.html')


# sign up
# @return status
@app.route('/signup', methods=['POST'])
def signup():
    return signUp(request.json['username'], request.json['password'])


def signUp(username, password):
    if users.find_one({"username":username}) != None:
        return jsonify({'status': "fail", "message":"Cannot assingn this username"}), 401

    # need to add HASH and SALT to password.
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
    if user == None or not bcrypt.checkpw((password + user['salt'].decode()).encode() , user['password']):
        return make_response("Username not found or wrong password", 403, {'WWW-Authentic' : 'Basic realm:"Authentcation faild!'})

    session['logged_in'] = True

    token = {
        'user' : username,
        'secret' : jwt.encode({'pass' : password, 'user' : username,
                'expiration' : str(datetime.utcnow() + timedelta(seconds=120))}, app.config['SECRET_KEY'], algorithm="HS256")
    }

    return jsonify({'token' : token}), 200


@app.route('/createTrip', methods=['POST'])
# @return tripID
def createTrip():
    #this is from ron
    # trip = createTrip()
    print(request.json)
    flags = request.json['flags']
    trip = tripAlgo.getTrip(request.json['srcAirport'], request.json['startDate'], request.json['duration'], request.json['numOfPeople'], flags['isFastPaced'], flags['isMuseumOriented'], flags['isLuxuriance'], flags['isLowCost'], request.json['destination'])
    tripJSON = TripToJson(trip)
    return tripJSON, 200

    # trip = classes.Trip()
    trip = classes.Trip(1,2,3,4,5,6)
    return insertTrip(trip)



@app.route("/insertTripToUser", methods=['POST'])
@token_required
def insertTripToUser():
    try:
        trip = JsonToTrip(request.json["trip"])

        tripID = insertTrip(trip)

        addTripToUser(request.json["token"]["user"], tripID)
        return 200
    except:
        return "Cannot insert trip", 403



# @return tripID
def insertTrip(trip):
    trip = classes.Trip.toTrip(trip)
    
    tripDays = []
    for day in trip.days:
        tripDays.append(insertDay(day))
        
    trip.days = tripDays


    # set the user of the trip
    user = users.find_one({"username" : request.json["token"]["user"]})
    trip.userId = user["_id"]

    newFlights = []
    for flight in trip.initFlight:
        newFlights.append(flight.__dict__)
    trip.initFlight = newFlights

    newflights2 = []
    for flight in trip.finFlight:
     newflights2.append(flight.__dict__)
    trip.finFlight = newflights2
    
    return trips.insert_one(trip.__dict__) 


# @return dayID
def insertDay(day):
    day = classes.Day.toDay(day)
    activityIDS = []
    transIDS = []
    placeID = []

    for activitiy in day.activities:
        activityIDS.append(activities.insert_one({'activity':activitiy.__dict__}).inserted_id)

    for trans in day.transportation:
        transIDS.append(transportations.insert_one({'transformation':trans.__dict__}).inserted_id)

    placeID = placeOfStay.insert_one({'placeOfStay':day.placeOfStay.__dict__}).inserted_id

    day.activities = activityIDS
    day.transportation = transIDS
    day.placeOfStay = placeID
    day = day.__dict__

    return days.insert_one(day).inserted_id




@app.route('/getTrip', methods=['POST'])
@token_required
def GetTrip():
    # return getTrip(request.args.get('tripID'))
    try:
        return getTrip(request.json['tripID']), 200
    except:
        return "Cant get trip", 403
    


# @return trip object
def getTrip(id):
    trip = trips.find_one({'_id':id})
    trip = classes.Trip.DictToTrip(trip)

    tripDays = []
    for day in trip.days:
        tripDays.append(getDay(day))

    trip.days = tripDays

    newFlights = []
    for flight in trip.initFlight:
        newFlights.append(classes.Transport.DictToTransport(flight))
    trip.initFlight = newFlights

    newFlights2 = []
    for flight in trip.finFlight:
        newFlights2.append(classes.Transport.DictToTransport(flight))
    trip.finFlight = newFlights2

    return trip


# @return day object
def getDay(dayID):
    day = days.find_one({'_id':dayID})
    day = classes.Day.DictToDay(day)

    activityObjects = []
    for activity in day.activities:
        act = activities.find_one({'_id':activity})
        act = classes.Activity.DictToActivity(act['activity'])
        activityObjects.append(act)

    transObjects = []
    for trans in day.transportation:
        transformation = transportations.find_one({'_id':trans})
        transformation = classes.Transport.DictToTransport(transformation['transformation'])
        transObjects.append(transformation)
    
    placeOf = placeOfStay.find_one({'_id':day.placeOfStay})
    placeOf = classes.PlaceOfStay.DictToPlace(placeOf['placeOfStay'])

    day.activities = activityObjects
    day.transportation = transObjects
    day.placeOfStay = placeOf

    return day




@app.route('/updateTrip', methods=['POST'])
@token_required
def UpdateTrip():
    try:
        return updateTrip(request.json['tripID'], request.json['trip']), 200
    except:
        return "Cant update trip", 403


def updateTrip(tripId, newTrip):
    newTrip = classes.Trip.DictToTrip(newTrip)
    return trips.find_one_and_update({'_id':tripId}, {'$set':newTrip.__dict__})




############### out of use ###############
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

        for trip in user['trips']:
            trips.append({'id':trip, 'name':getTrip(trip).name})
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
        trips.append(getTrip(trip))

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
    
    if (not type(user['trips']) == list):
        user['trips'] = [tripID]

    else:
        if (tripID in user['trips']):
            return
        user['trips'] = user['trips'] + [tripID]

    user = users.find_one_and_update({"username" : name}, update={ "$set": {"trips" : user['trips']}})




@app.route('/removeTripFromUser', methods=['POST'])
@token_required
def RemoveTripFromUser():
    try:
        return removeTripfromUser(request.json['username'], request.json['tripID']), 200
    except:
        return "Cant romve trip", 403


def removeTripfromUser(name, tripID):
    user = users.find_one({"username" : name})
    
    if (not type(user['trips']) == list):
        return

    else:
        if (tripID not in user['trips']):
            return

        user['trips'].remove(tripID)

    user = users.find_one_and_update({"username" : name}, update={ "$set": {"trips" : user['trips']}})



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
    # send ron request to update the trip
    # trip = ron.updateTrip(trip)
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


def mockTrip():
    activity1 = classes.Activity(2, 2000, str(datetime.now()), str(datetime.now()), "first activity", "location1", "image1", False)
    activity2 = classes.Activity(2, 2000, str(datetime.now()), str(datetime.now()), "second activity", "location2", "image2", False)
    myActivities = [activity1, activity2]

    myTransformation1 = classes.Transport(0.5, 7, str(datetime.now()),str(datetime.now()), "1->2", "location 1.5", "image 1.5", False, "first activity", 1, "second activity","first stat", "second stat")
    myTransformation2 = classes.Transport(0.5, 7, str(datetime.now()),str(datetime.now()), "1->2", "location 1.5", "image 1.5", False, "first activity", 1, "second activity","first stat", "second stat")
    myTransformation3 = classes.Transport(0.5, 7, str(datetime.now()),str(datetime.now()), "1->2", "location 1.5", "image 1.5", False, "first activity", 1, "second activity","first stat", "second stat")
    
    myPlace = classes.PlaceOfStay(1, 500, str(datetime.now()), str(datetime.now()), "hotel", "location sleep", "image sleep", True, "Israel")

    day1 = classes.Day(myActivities, [[myTransformation1]], 4507, str(datetime.now()),str(datetime.now()),4.5, myPlace)
    day2 = classes.Day(myActivities, [[myTransformation2]], 4507, str(datetime.now()),str(datetime.now()),4.5, myPlace)
    day3 = classes.Day(myActivities, [[myTransformation3]], 4507, str(datetime.now()),str(datetime.now()),4.5, myPlace)
    
    myDays = [day1, day2, day3]

    flight1 =classes.Transport(0.5, 7, str(datetime.now()),str(datetime.now()), "1->2", "location 1.5", "image 1.5", False, "first activity", 1, "second activity","first stat", "second stat")
    flight2 =classes.Transport(0.5, 7, str(datetime.now()),str(datetime.now()), "1->2", "location 1.5", "image 1.5", False, "first activity", 1, "second activity","first stat", "second stat")
    flight3 =classes.Transport(0.5, 7, str(datetime.now()),str(datetime.now()), "1->2", "location 1.5", "image 1.5", False, "first activity", 1, "second activity","first stat", "second stat")
    flight4 =classes.Transport(0.5, 7, str(datetime.now()),str(datetime.now()), "1->2", "location 1.5", "image 1.5", False, "first activity", 1, "second activity","first stat", "second stat")

    myTrip = classes.Trip("shaked4-Israel", "Israel", 3, str(datetime.now()), str(datetime.now()), myDays, 3*4507, ObjectId("ababcdcdefefababcdcdefef"),[flight1,flight2],[flight3,flight4])

    return myTrip

def printTripObject(tripID):
    trip = getTrip(tripID)
    print(trip.__dict__)
    print()
    print()
    for day in trip.days:
        print(day.__dict__)
        print()
        for act in day.activities:
            print(act.__dict__)
        print()
        for trans in day.transportation:
            print(trans.__dict__)
        print()
        print(day.placeOfStay.__dict__)


def TripToJson(trip):
    transOptions = {0 : "NONE", 1 : "BUS", 2 : "TRAIN", 3 : "RAM", 4 : "PUBLICTAXI", 5 : "FLIGHT"}


    newDays = []
    trip.endDate = str(trip.endDate)
    trip.startDate = str(trip.startDate)
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
        nFlight = flight.__dict__
        nFlight["methodOfTransportation"] = transOptions.get(int(nFlight["methodOfTransportation"]))
        newFlights.append(nFlight)
    trip.initFlight = newFlights

    newflights2 = []
    for flight in trip.finFlight:
        nFlight = flight.__dict__
        nFlight["methodOfTransportation"] = transOptions.get(int(nFlight["methodOfTransportation"]))
        newflights2.append(nFlight)
    trip.finFlight = newflights2
    return json.dumps(trip.__dict__)


def JsonToTrip(jsonTrip):
    transOptions = { "NONE" : 0, "BUS" : 1, "TRAIN" : 2, "RAM" : 3, "PUBLICTAXI" : 4, "FLIGHT" : 5}

    trip = json.loads(jsonTrip)
    newDays = []

    trip['endDate'] = datetime.strptime(trip['endTime'], '%Y-%m-%dT%H:%M:%S')
    trip['startDate'] = datetime.strptime(trip['startDate'], '%Y-%m-%dT%H:%M:%S')

    for day in trip['days']:

        day['timeStart'] = datetime.strptime(day['timeStart'], '%Y-%m-%dT%H:%M:%S')
        day['timeEnd'] = datetime.strptime(day['timeEnd'], '%Y-%m-%dT%H:%M:%S')

        newacts = []
        for act in day['activities']:
            act['timeStart'] = datetime.strptime(act['timeStart'], '%Y-%m-%dT%H:%M:%S')
            act['timeEnd'] = datetime.strptime(act['timeEnd'], '%Y-%m-%dT%H:%M:%S')

            actson = classes.Activity.DictToActivity(act)
            newacts.append(actson)
        day['activities'] = newacts

        newtrans = []
        for trans in day["transportation"]:
            subtrans = []
            for trn in trans:
                trn['timeStart'] = datetime.strptime(trn['timeStart'], '%Y-%m-%dT%H:%M:%S')
                trn['timeEnd'] = datetime.strptime(trn['timeEnd'], '%Y-%m-%dT%H:%M:%S')

                transon = classes.Transport.DictToTransport(trn)

                transon.methodOfTransportation = transOptions[transon.methodOfTransportation]

                subtrans.append(transon)
            newtrans.append(subtrans)
        day["transportation"] = newtrans


        day["placeOfStay"]["timeStart"] = datetime.strptime(day["placeOfStay"]["timeStart"], '%Y-%m-%dT%H:%M:%S')
        day["placeOfStay"]["timeEnd"] = datetime.strptime(day["placeOfStay"]["timeEnd"], '%Y-%m-%dT%H:%M:%S')

        day["placeOfStay"] = classes.PlaceOfStay.DictToPlace(day["placeOfStay"])

        newday = classes.Day.DictToDay(day)
        newDays.append(newday)

    trip['days'] = newDays

    trip['userId'] = ObjectId(trip['userId'])

    newFlights = []
    for flight in trip["initFlight"]:
        newFlights.append(classes.Transport.DictToTransport(flight))
    trip["initFlight"] = newFlights

    newFlights2 = []
    for flight in trip["finFlight"]:
        newFlights2.append(classes.Transport.DictToTransport(flight))
    trip["finFlight"] = newFlights2
    
    return classes.Trip.DictToTrip(trip)


if __name__ == '__main__':
    app.run(debug=True)
    # print(signUp("shaked", "moked"))
    # print(signIn("shaked", "moked"))
    # input()
    # print(changePassword("shaked", "moked", "noded"))
    # print(signUp("shaked4", "moked"))
    # print(signIn("shaked4", "moked"))
    # print(Trips())

    # myTrip = mockTrip()
    # myTrip2 = mockTrip()


    # tripID = insertTrip(myTrip2).inserted_id


    # trip = trips.find_one({'_id':tripID})
    # trip = trips.find_one({'_id':ObjectId('6283b41a23876f4403012a2b')})
    # print(trip)
    # trip = trips.find_one({'destination':'Israel'})
    # print(trip)

    # printTripObject(tripID)


    # # trip-user
    # print(getTripsByusername("shaked4"))
    # addTripToUser("shaked4", ObjectId('6296391a2a9317f48543073f'))
    # addTripToUser("shaked4", ObjectId('62963935ed1317e541f491be'))
    # addTripToUser("shaked4", ObjectId('6283b41a23876f4403012a2b'))
    # print(getTripsByusername("shaked4"))
    # removeTripfromUser("shaked4", ObjectId('62963935ed1317e541f491be'))
    # print(getTripsByusername("shaked4"))
    # request.json['username'] = "shaked4"s
    # print(GetTripsAndNamesByUser())
    # print(getTripsByusername("shaked4"))

    # t = mockTrip()
    # t = TripToJson(t)
    # parsed = json.loads(t)
    # print(json.dumps(parsed, indent=4, sort_keys=True))

    # trip = JsonToTrip(t)
    

    

