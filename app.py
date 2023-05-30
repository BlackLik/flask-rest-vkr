import pickle
from flask import Flask, jsonify, request
from api import api
from flask_cors import CORS
from dotenv import load_dotenv

app = Flask(__name__)
CORS(app)
load_dotenv()
app.register_blueprint(api, url_prefix='/api')


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
