# test server to use as backend for fronntend testings
from __future__ import print_function
from flask import Flask , request, jsonify,make_response
from datetime import datetime
import csv

# server
app = Flask(__name__)
app.config['SECRET_KEY'] = '03a5t89c1pf9Uc0a0f7E'

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


@app.route('/signup', methods=['POST'])
def signup():
    return signUp(request.json['username'], request.json['password'])


def signUp(username, password):
    print("\nNew user trying to sign up:\nUsername:" + username + "\nPassword:" + password)
    return jsonify({'status': "successful", "message": "User created successfuly"}), 200


@app.route('/signup-fail', methods=['POST'])
def signup_fail():
    x = jsonify({'status': "fail", "message":"Cannot assingn this username"}), 401
    print(x)
    return x

@app.route('/signin-fail', methods=['POST'])
def signin_fail():
    x = make_response("Username not found or wrong password", 403, {'WWW-Authentic' : 'Basic realm:"Authentcation faild!'})
    print(x)
    return x


@app.route('/signin', methods=['POST'])
def signin():
    return signIn(request.json['username'], request.json['password'])


def signIn(username, password):
    print("\nA user trying to sign in:\nUsername:" + username + "\nPassword:" + password)
    token = {
        'user' : username,
    }
    print(token)

    return jsonify({'token' : token})


@app.route('/getTrip', methods=['POST'])
def getTrip():
    id = request.json['tripID'];
    return trip(id), 200


def trip(id):
    return jsonify({
        'id' : id,
        'name' : 'for display',
        'cost' : 11111,
        'duration' : 3,
        'userId' : 1234,
        'endDate' : datetime.now(),
        'startDate' : datetime.now(),
        "initFlight": [{
            "duration" : 2.5,
            "cost" : "8987.28",
            "timeStart" : "2022-07-07 11:35:00",
            "timeEnd" : "2022-07-07 14:05:00",
            "title" : "AZ61",
            "originLink" : "",
            "destinationLink" : "",
            "orderInAdvance" : True,
            "placeOfOrigin" : "",
            "methodOfTransportation" : "FLIGHT",
            "destination" : "",
            "baseStation" : "MAD-2",
            "arrivalStation": "FCO"
        }, {
            "duration": 3.3333333333333335,
            "cost" : 0,
            "timeStart" : "2022-08-07 09:50:00",
            "timeEnd" : "2022-08-07 13:10:00",
            "title" : "AZ614",
            "originLink" : "",
            "destinationLink" : "",
            "orderInAdvance" : True,
            "placeOfOrigin" : "",
            "methodOfTransportation" : "FLIGHT",
            "destination" : "",
            "baseStation" : "FCO-3",
            "arrivalStation" : "BOS"
        }, {
            "duration": 3.3333333333333335,
            "cost" : 0,
            "timeStart" : "2022-08-07 09:50:00",
            "timeEnd" : "2022-08-07 13:10:00",
            "title" : "PJ653",
            "originLink" : "",
            "destinationLink" : "",
            "orderInAdvance" : True,
            "placeOfOrigin" : "",
            "methodOfTransportation" : "FLIGHT",
            "destination" : "",
            "baseStation" : "BOS",
            "arrivalStation" : "FML"
        }],
        "finFlight" : [],
        'days' : [{
            'cost' : 123,
            'duration' : 1.5,
            'timeStart' : datetime.now(),
            'timeEnd' : datetime.now(),
            'placeOfStay' : {
                'cost' : 50,
                'destination' : '33.333333,55.555555',
                'duration' : 1,
                'images' : ['https://www.danhotels.co.il/sites/default/files/styles/full_page_3_8/public/2018-08/DTGallery1.jpg?itok=0_WynAai', 'https://upload.wikimedia.org/wikipedia/commons/1/19/TelAM.jpg'],
                'link' : ['https://www.google.co.il/travel/hotels/entity/CgsI74CAlc6F1erQARAB?g2lb=2502405%2C2502548%2C4208993%2C4254308%2C4258168%2C4260007%2C4270442%2C4271060%2C4274032%2C4285990%2C4288513%2C4289525%2C4291318%2C4296668%2C4301054%2C4302823%2C4305595%2C4308216%2C4313006%2C4314836%2C4315873%2C4317816%2C4317915%2C4324289%2C4329288%2C4329495%2C4333234%2C4270859%2C4284970%2C4291517%2C4292955%2C4316256%2C4333106&hl=iw&gl=il&un=1&rp=EPOJxP-ega-d9QE4AUAASAE&ictx=1&sa=X&tcfs=EhoaGAoKMjAxOS0xMS0yNxIKMjAxOS0xMS0yOFIA&utm_campaign=sharing&utm_medium=link&utm_source=htls&ts=CAESABp9Cl8SWzIlMHgxNTFlYTBmNTEzZDk0ZDBiOjB4ZjUzYWJjMDllZmYxMDRmMzoy15DXptecINeQ157Xmdeo15Qg15XXkifXldeo15InINeX15PXqNeZINeQ15nXqNeV15caABIaEhQKBwjmDxAIGBsSBwjmDxAIGBwYATICEAAqCwoHKAE6A0lMUxoA&ap=iAEC&ved=0CAAQ5JsGahcKEwiQ4s3y9an4AhUAAAAAHQAAAAAQAw'],
                'orderInAdvance' : True,
                'title' : 'DAN Hotel'
            },
            'transportation' : [[{
                'cost' : 7,
                'destination' : '33.333333,55.555555',
                'duration' : 0.5,
                'orderInAdvance' : False,
                'link' : ['https://www.google.com/maps/dir//32.065685,34.785309'],
                'methodOfTransportation' : 'Bus',
                'placeOfOrigin' : '66.666666,77.777777',
                'title' : '1->1.5',
                'timeStart' : datetime.now(),
                'timeEnd' : datetime.now(),
                'baseStation': 'stat1',
                'arrivalStation': 'stat2',
                'originLink': 'https://translate.google.co.il/?hl=iw&sl=iw&tl=en&op=translate',
                'destinationLink': 'https://github.com/'
            }, {
                'cost' : 7,
                'destination' : '33.333333,55.555555',
                'duration' : 0.5,
                'orderInAdvance' : False,
                'link' : ['https://www.google.com/maps/dir//32.065685,34.785309'],
                'methodOfTransportation' : 'Bus',
                'placeOfOrigin' : '66.666666,77.777777',
                'title' : '1.5->2',
                'timeStart' : datetime.now(),
                'timeEnd' : datetime.now(),
                'baseStation': 'stat1',
                'arrivalStation': 'stat2',
                'originLink': 'https://translate.google.co.il/?hl=iw&sl=iw&tl=en&op=translate',
                'destinationLink': 'https://github.com/'
            }]],
            'activities' : [{
                'cost' : 250,
                'duration' : 2,
                'orderInAdvance' : True,
                'images' : ['https://upload.wikimedia.org/wikipedia/commons/1/19/TelAM.jpg'],
                'link' : ['https://www.google.co.il/maps/place/%D7%9E%D7%95%D7%96%D7%99%D7%90%D7%95%D7%9F+%D7%AA%D7%9C+%D7%90%D7%91%D7%99%D7%91+%D7%9C%D7%90%D7%9E%D7%A0%D7%95%D7%AA%E2%80%AD/@32.0771846,34.7906177,17z/data=!3m1!4b1!4m5!3m4!1s0x151d4b9b02453fa7:0xf74ba430787ab813!8m2!3d32.0771761!4d34.7861374?hl=iw'],
                'title' : 'act1',
                'destination' : '33.333333,55.555555',
                'timeStart' : datetime.now(),
                'timeEnd' : datetime.now()
            },
            {
                'cost' : 500,
                'duration' : 1,
                'orderInAdvance' : False,
                'images' : ['https://lh3.googleusercontent.com/-QHtkHHHbqUk/TuO2c92cf2I/AAAAAAAACw8/XBstONxlmOI/s1600/museum-03.jpg?gl=IL'],
                'link' : ['https://www.google.co.il/maps/place/%D7%9E%D7%95%D7%96%D7%99%D7%90%D7%95%D7%9F+%D7%AA%D7%9C+%D7%90%D7%91%D7%99%D7%91+%D7%9C%D7%90%D7%9E%D7%A0%D7%95%D7%AA%E2%80%AD/@32.0771846,34.7906177,17z/data=!3m1!4b1!4m5!3m4!1s0x151d4b9b02453fa7:0xf74ba430787ab813!8m2!3d32.0771761!4d34.7861374?hl=iw'],
                'title' : 'act2',
                'destination' : '33.333333,55.555555',
                'timeStart' : datetime.now(),
                'timeEnd' : datetime.now()
            }]
        },
        {
            'cost' : 1200,
            'duration' : 3,
            'timeStart' : datetime.now(),
            'timeEnd' : datetime.now(),
            'placeOfStay' : {
                'cost' : 50,
                'destination' : '33.333333,55.555555',
                'duration' : 1,
                'images' : ['https://www.danhotels.co.il/sites/default/files/styles/full_page_3_8/public/2018-08/DTGallery1.jpg?itok=0_WynAai'],
                'link' : ['https://www.google.co.il/travel/hotels/entity/CgsI74CAlc6F1erQARAB?g2lb=2502405%2C2502548%2C4208993%2C4254308%2C4258168%2C4260007%2C4270442%2C4271060%2C4274032%2C4285990%2C4288513%2C4289525%2C4291318%2C4296668%2C4301054%2C4302823%2C4305595%2C4308216%2C4313006%2C4314836%2C4315873%2C4317816%2C4317915%2C4324289%2C4329288%2C4329495%2C4333234%2C4270859%2C4284970%2C4291517%2C4292955%2C4316256%2C4333106&hl=iw&gl=il&un=1&rp=EPOJxP-ega-d9QE4AUAASAE&ictx=1&sa=X&tcfs=EhoaGAoKMjAxOS0xMS0yNxIKMjAxOS0xMS0yOFIA&utm_campaign=sharing&utm_medium=link&utm_source=htls&ts=CAESABp9Cl8SWzIlMHgxNTFlYTBmNTEzZDk0ZDBiOjB4ZjUzYWJjMDllZmYxMDRmMzoy15DXptecINeQ157Xmdeo15Qg15XXkifXldeo15InINeX15PXqNeZINeQ15nXqNeV15caABIaEhQKBwjmDxAIGBsSBwjmDxAIGBwYATICEAAqCwoHKAE6A0lMUxoA&ap=iAEC&ved=0CAAQ5JsGahcKEwiQ4s3y9an4AhUAAAAAHQAAAAAQAw'],
                'orderInAdvance' : True,
                'title' : 'DAN Hotel'
            },
            'transportation' : [[{
                'cost' : 7,
                'destination' : '33.333333,55.555555',
                'duration' : 0.5,
                'orderInAdvance' : False,
                'link' : ['https://www.google.com/maps/dir//32.065685,34.785309'],
                'methodOfTransportation' : 'Bus',
                'placeOfOrigin' : '66.666666,77.777777',
                'title' : '1->2',
                'timeStart' : datetime.now(),
                'timeEnd' : datetime.now(),
                'baseStation': 'stat1',
                'arrivalStation': 'stat2',
                'originLink': 'https://translate.google.co.il/?hl=iw&sl=iw&tl=en&op=translate',
                'destinationLink': 'https://github.com/'
            }]],
            'activities' : [{
                'cost' : 250,
                'duration' : 2,
                'orderInAdvance' : False,
                'images' : ['https://upload.wikimedia.org/wikipedia/commons/1/19/TelAM.jpg'],
                'link' : ['https://www.google.co.il/maps/place/%D7%9E%D7%95%D7%96%D7%99%D7%90%D7%95%D7%9F+%D7%AA%D7%9C+%D7%90%D7%91%D7%99%D7%91+%D7%9C%D7%90%D7%9E%D7%A0%D7%95%D7%AA%E2%80%AD/@32.0771846,34.7906177,17z/data=!3m1!4b1!4m5!3m4!1s0x151d4b9b02453fa7:0xf74ba430787ab813!8m2!3d32.0771761!4d34.7861374?hl=iw'],
                'title' : 'act1',
                'destination' : '33.333333,55.555555',
                'timeStart' : datetime.now(),
                'timeEnd' : datetime.now()
            },
            {
                'cost' : 500,
                'duration' : 1,
                'orderInAdvance' : False,
                'images' : ['https://lh3.googleusercontent.com/-QHtkHHHbqUk/TuO2c92cf2I/AAAAAAAACw8/XBstONxlmOI/s1600/museum-03.jpg?gl=IL'],
                'link' : ['https://www.google.co.il/maps/place/%D7%9E%D7%95%D7%96%D7%99%D7%90%D7%95%D7%9F+%D7%AA%D7%9C+%D7%90%D7%91%D7%99%D7%91+%D7%9C%D7%90%D7%9E%D7%A0%D7%95%D7%AA%E2%80%AD/@32.0771846,34.7906177,17z/data=!3m1!4b1!4m5!3m4!1s0x151d4b9b02453fa7:0xf74ba430787ab813!8m2!3d32.0771761!4d34.7861374?hl=iw'],
                'title' : 'act2',
                'destination' : '33.333333,55.555555',
                'timeStart' : datetime.now(),
                'timeEnd' : datetime.now()
            }]
        }, {
            'cost' : 123,
            'duration' : 1.5,
            'timeStart' : datetime.now(),
            'timeEnd' : datetime.now(),
            'placeOfStay' : {
                'cost' : 50,
                'destination' : '33.333333,55.555555',
                'duration' : 1,
                'images' : ['https://www.danhotels.co.il/sites/default/files/styles/full_page_3_8/public/2018-08/DTGallery1.jpg?itok=0_WynAai'],
                'link' : ['https://www.google.co.il/travel/hotels/entity/CgsI74CAlc6F1erQARAB?g2lb=2502405%2C2502548%2C4208993%2C4254308%2C4258168%2C4260007%2C4270442%2C4271060%2C4274032%2C4285990%2C4288513%2C4289525%2C4291318%2C4296668%2C4301054%2C4302823%2C4305595%2C4308216%2C4313006%2C4314836%2C4315873%2C4317816%2C4317915%2C4324289%2C4329288%2C4329495%2C4333234%2C4270859%2C4284970%2C4291517%2C4292955%2C4316256%2C4333106&hl=iw&gl=il&un=1&rp=EPOJxP-ega-d9QE4AUAASAE&ictx=1&sa=X&tcfs=EhoaGAoKMjAxOS0xMS0yNxIKMjAxOS0xMS0yOFIA&utm_campaign=sharing&utm_medium=link&utm_source=htls&ts=CAESABp9Cl8SWzIlMHgxNTFlYTBmNTEzZDk0ZDBiOjB4ZjUzYWJjMDllZmYxMDRmMzoy15DXptecINeQ157Xmdeo15Qg15XXkifXldeo15InINeX15PXqNeZINeQ15nXqNeV15caABIaEhQKBwjmDxAIGBsSBwjmDxAIGBwYATICEAAqCwoHKAE6A0lMUxoA&ap=iAEC&ved=0CAAQ5JsGahcKEwiQ4s3y9an4AhUAAAAAHQAAAAAQAw'],
                'orderInAdvance' : True,
                'title' : 'DAN Hotel'
            },
            'transportation' : [[{
                'cost' : 7,
                'destination' : '33.333333,55.555555',
                'duration' : 0.5,
                'orderInAdvance' : False,
                'link' : ['https://www.google.com/maps/dir//32.065685,34.785309'],
                'methodOfTransportation' : 'Bus',
                'placeOfOrigin' : '66.666666,77.777777',
                'title' : '1->1.5',
                'timeStart' : datetime.now(),
                'timeEnd' : datetime.now(),
                'baseStation': 'stat1',
                'arrivalStation': 'stat2',
                'originLink': 'https://translate.google.co.il/?hl=iw&sl=iw&tl=en&op=translate',
                'destinationLink': 'https://github.com/'
            }], [{
                'cost' : 7,
                'destination' : '33.333333,55.555555',
                'duration' : 0.5,
                'orderInAdvance' : False,
                'link' : ['https://www.google.com/maps/dir//32.065685,34.785309'],
                'methodOfTransportation' : 'Bus',
                'placeOfOrigin' : '66.666666,77.777777',
                'title' : '1.5->2',
                'timeStart' : datetime.now(),
                'timeEnd' : datetime.now(),
                'baseStation': 'stat1',
                'arrivalStation': 'stat2',
                'originLink': 'https://translate.google.co.il/?hl=iw&sl=iw&tl=en&op=translate',
                'destinationLink': 'https://github.com/'
            }]],
            'activities' : [{
                'cost' : 250,
                'duration' : 2,
                'orderInAdvance' : True,
                'images' : ['https://upload.wikimedia.org/wikipedia/commons/1/19/TelAM.jpg'],
                'link' : ['https://www.google.co.il/maps/place/%D7%9E%D7%95%D7%96%D7%99%D7%90%D7%95%D7%9F+%D7%AA%D7%9C+%D7%90%D7%91%D7%99%D7%91+%D7%9C%D7%90%D7%9E%D7%A0%D7%95%D7%AA%E2%80%AD/@32.0771846,34.7906177,17z/data=!3m1!4b1!4m5!3m4!1s0x151d4b9b02453fa7:0xf74ba430787ab813!8m2!3d32.0771761!4d34.7861374?hl=iw'],
                'title' : 'act1',
                'destination' : '33.333333,55.555555',
                'timeStart' : datetime.now(),
                'timeEnd' : datetime.now()
            },
            {
                'cost' : 500,
                'duration' : 1,
                'orderInAdvance' : False,
                'images' : ['https://lh3.googleusercontent.com/-QHtkHHHbqUk/TuO2c92cf2I/AAAAAAAACw8/XBstONxlmOI/s1600/museum-03.jpg?gl=IL'],
                'link' : ['https://www.google.co.il/maps/place/%D7%9E%D7%95%D7%96%D7%99%D7%90%D7%95%D7%9F+%D7%AA%D7%9C+%D7%90%D7%91%D7%99%D7%91+%D7%9C%D7%90%D7%9E%D7%A0%D7%95%D7%AA%E2%80%AD/@32.0771846,34.7906177,17z/data=!3m1!4b1!4m5!3m4!1s0x151d4b9b02453fa7:0xf74ba430787ab813!8m2!3d32.0771761!4d34.7861374?hl=iw'],
                'title' : 'act2',
                'destination' : '33.333333,55.555555',
                'timeStart' : datetime.now(),
                'timeEnd' : datetime.now()
            }]
        }]
    })


@app.route('/getTripsAndNamesByUser', methods=['POST'])
def getTripsByusername():
    user = request.json['username']
    print("\nRequested user trips: " + user)
    trips = []
    for i in range(1, 9):
        trips.append({"id":i, "name":f'trip{i}'})
    print(trips)

    return jsonify(trips), 200


@app.route('/getTripsAndNamesByUser-fail', methods=['POST'])
def getTripsByusernameFail():
    return jsonify({}), 405


@app.route('/insertTripToUser', methods=['POST'])
def insertTrip():
    return jsonify({}), 200


@app.route('/insertTripToUser-fail', methods=['POST'])
def insertTripFail():
    return jsonify({}), 404

@app.route('/removeTripFromUser', methods=['POST'])
def RemoveTripFromUser():
    return jsonify({}), 200

@app.route('/removeTripFromUser-fail', methods=['POST'])
def RemoveTripFromUserFail():
    return "Cant romve trip", 403

@app.route('/getAirportsAndDistrictsLists', methods=['GET'])
def getAirportsAndDistrictsLists():
    print(_regionsMap[0])
    return jsonify({ 'airportsMap' : _airportsMap, 'countriesMap' : _countriesMap, 'regionsMap' : _regionsMap }), 200

@app.route('/createTrip', methods=['POST'])
def createTrip():
    return trip(''), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)
