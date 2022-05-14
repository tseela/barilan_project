# test server to use as backend for fronntend testings

from flask import Flask , request, jsonify,make_response, render_template
import jwt
from datetime import datetime, timedelta

# server
app = Flask(__name__)
app.config['SECRET_KEY'] = '03a5t89c1pf9Uc0a0f7E'


@app.route('/signup', methods=['POST'])
def signup():
    return signUp(request.json['username'], request.json['password'])


def signUp(username, password):
    print("\nNew user trying to sign up:\nUsername:" + username + "\nPassword:" + password)
    return signIn(username, password)




@app.route('/signin', methods=['POST'])
def signin():
    return signIn(request.json['username'], request.json['password'])


def signIn(username, password):
    print("\nA user trying to sign in:\nUsername:" + username + "\nPassword:" + password)
    token = ({
        'user' : username,
        'expiration' : str(datetime.utcnow() + timedelta(seconds=120))
    },
    app.config['SECRET_KEY'])
    print(token)

    return jsonify({'token' : token})


if __name__ == '__main__':
    app.run(debug=True, port=5000)
