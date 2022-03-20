from flask import Flask

app = Flask(__name__)


@app.route('/api', methods=['GET'])
def home():
    return {
        'name': 'ola amigos'
    }


if __name__ == '__main__':
    app.run(debug=True)
