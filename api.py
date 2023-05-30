import pickle
from flask import Blueprint, request, jsonify
from function import check_main_params
import config
import requests

api = Blueprint('api', __name__, url_prefix='/api')



@api.route('/')
def index():
    req = requests.get('https://api.ipify.org/?format=json')
    return jsonify({'message': req.json()}), 200

@api.route('/predict', methods=['POST'])
def predict():
    data = request.json
    result = check_main_params(data=data)
    if result is not None:
        return result
    
    
    
    
    
    return jsonify({'message': "Hello, world!"}), 200
