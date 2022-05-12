# from flask import Flask
# import pymongo
from flask import Flask , request, jsonify,make_response, render_template, session
import jwt
from datetime import datetime, timedelta
from functools import wraps

import pymongo
from flask_bcrypt import bcrypt


# server
app = Flask(__name__)
app.config['SECRET_KEY'] = '03a5t89c1pf9Uc0a0f7E'
# db
client = pymongo.MongoClient("mongodb://TripDesigner:ShakedKing@tripdesigner-shard-00-00.i9pia.mongodb.net:27017,tripdesigner-shard-00-01.i9pia.mongodb.net:27017,tripdesigner-shard-00-02.i9pia.mongodb.net:27017/Users?ssl=true&replicaSet=atlas-517ql2-shard-0&authSource=admin&retryWrites=true&w=majority")
db = client.tripDesigner
users = db.Users
trips = db.Trips


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
        token = request.args.get('token')
        if not token:
            return jsonify({'Alert!' : 'Token is missing!'})
        try :
            payload = jwt.decode(token, app.config['SECRET_KEY'])
        except:
            return jsonify({'Alert!' : 'Invalid Token!'})
        
    return decorated
            



# acttualy the 'then' statements need to be what Tseela want.
@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('homePage.html')
    else:
        return render_template('trips.html')



@app.route('/trips')
@token_required
def Trips():
    return render_template('trips.html')


@app.route('/signup', methods=['POST'])
def signup():
    return signUp(request.form['username'], request.form['password'])


def signUp(username, password):
    if users.find_one({"username":username}) != None:
        return jsonify({'status': "fail", "message":"Cannot assingn this username"}), 401

    # need to add HASH and SALT to password.
    user = {
        "username" : username,
        "password" : bcrypt.generate_password_hash[password.decode('utf-8')],
        "trips" : []
    }
    users.insert_one(user)
    return jsonify({'status': "successful", "message": "User created successfuly"}), 200




@app.route('/signin', methods=['POST'])
def signin():
    return signIn(request.form['username'], request.form['password'])


def signIn(username, password):
    user = users.find_one({"username":username})

    if user == None or not bcrypt.check_password_hash(user['password'], password):
        return make_response("Username not found or wrong password", 403, {'WWW-Authentic' : 'Basic realm:"Authentcation faild!'})

    session['logged_in'] = True

    token = jwt.encode({
        'user' : username,
        'expiration' : str(datetime.utcnow() + timedelta(seconds=120))
    },
    app.config['SECRET_KEY'])

    return jsonify({'token' : token.decode('utf-8')})

'''
@app.route('/createtrip')
@token_required
def Trips():
    #this is from ron
    trip = classes.Trip(creatrTrip())
    trips.insert_one(trip)
    return render_template('trips.html')
'''



# @app.route('/changePassword', methods=['POST'])
# def changepassword():
#     return changePassword(request.form['username'], request.form['password'], request.form['newPassword'])

 
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
#     return changeUsername(request.form['username'], request.form['password'], request.form['newUsername'])


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


if __name__ == '__main__':
    app.run(debug=True)
    # print(signUp("shaked", "moked"))
    # print(signIn("shaked", "moked"))
    # input()
    # print(changePassword("shaked", "moked", "noded"))
