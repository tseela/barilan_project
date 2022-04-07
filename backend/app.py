from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import pymongo

# server
app = Flask(__name__)
# db
client = pymongo.MongoClient("mongodb://TripDesigner:ShakedKing@tripdesigner-shard-00-00.i9pia.mongodb.net:27017,tripdesigner-shard-00-01.i9pia.mongodb.net:27017,tripdesigner-shard-00-02.i9pia.mongodb.net:27017/Users?ssl=true&replicaSet=atlas-517ql2-shard-0&authSource=admin&retryWrites=true&w=majority")
db = client.tripDesigner
users = db.Users


# example
@app.route('/api', methods=['GET','POST'])
def home():
    return {
        'name': 'ola amigos'
    }

@app.route('/signUp', methods=['GET','POST'])
def signUp(username, password):
    if users.find_one({"username":username}) != None:
        return "Cannot assingn this username"

    # need to add HASH and SALT to password.
    user = {
        "username" : username,
        "password" : password,
        "trips" : []
    }
    users.insert_one(user)
    return "ok"


@app.route('/signIn', methods=['GET','POST'])
def signIn(username, password):
    user = users.find_one({"username":username})
    if user == None:
        return "Username not found"
    if user["password"] != password:
        return "Wrong password"
    return "ok"

@app.route('/changePassword', methods=['GET','POST'])
def changePassword(username, password, newPassword):
    user = users.find_one({"username":username})
    if user == None:
        return "Username not found"
    if user["password"] != password:
        return "Wrong password"
    if password == newPassword:
        return "New password cannot be equals to old password"
    users.find_one_and_update({"username":username}, update={ "$set": {"password":newPassword}})
    return "ok"

@app.route('/changeUsername', methods=['GET','POST'])
def changeUsername(username, password, newUsername):
    user = users.find_one({"username":username})
    if user == None:
        return "Username not found"
    if user["password"] != password:
        return "Wrong password"
    if username == newUsername:
        return "New username cannot be equals to old username"
    users.find_one_and_update({"username":username}, update={ "$set": {"username":newUsername}})
    return "ok"


if __name__ == '__main__':
    # app.run(debug=True)
    # print(signUp("shaked", "moked"))
    # print(signIn("shaked", "moked"))
    # input()
    print(changePassword("shaked", "moked", "noded"))
