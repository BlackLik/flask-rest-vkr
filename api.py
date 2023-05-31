import pickle
from flask import Blueprint, request, jsonify
import function as fn
from model import User, Regions, Genders, ModelsPrediction
from functools import wraps
import requests


api = Blueprint('api', __name__, url_prefix='/api')
tfidfvectorizer_educational_organization = fn.loader_tfidfvectorizer('educational_organization')
tfidfvectorizer_qualification = fn.loader_tfidfvectorizer('qualification')


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        result = fn.check_user_params(request.json)
        if result is not None:
            return result
        return f(*args, **kwargs)
    return decorated_function


@api.route('/', methods=['POST'])
@login_required
def index():
    data = 'active'
    # req = requests.get('http://127.0.0.1:5000/api/users')
    return jsonify({'message': data}), 200


@api.route('/users', methods=['GET'])
def users():
    users = User.query.all()
    return jsonify({'users': [user.to_json() for user in users]}), 200


@api.route('/users/<int:user_id>', methods=['GET'])
def user(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return jsonify({'message': 'User not found'}), 404
    return jsonify({'user': user.to_json()}), 200


@api.route('/regions', methods=['GET'])
def regions():
    regions = Regions.query.all()
    return jsonify({'regions': [region.to_json() for region in regions]}), 200


@api.route('/regions/<int:region_id>', methods=['GET'])
def region(region_id):
    region = Regions.query.filter_by(id=region_id).first()
    return jsonify({'region': region.to_json()}), 200


@api.route('/genders', methods=['GET'])
def genders():
    genders = Genders.query.all()
    return jsonify({'genders': [gender.to_json() for gender in genders]}), 200


@api.route('/genders/<int:gender_id>', methods=['GET'])
def gender(gender_id):
    gender = Genders.query.filter_by(id=gender_id).first()
    return jsonify({'gender': gender.to_json()}), 200


@api.route('/predict', methods=['POST'])
@login_required
def predict():
    data = request.json
    result = fn.check_main_params(data=data)
    if result is not None:
        return result
    
    model_object = ModelsPrediction.query.filter_by(id_region=data['region'], id_gender=data['gender']).first()
    if model_object is None:
        return jsonify({'message': 'Model not found'}), 404
    
    educational_organization = data['educational_organization'].lower().strip().split(' ')
    qualification = data['qualification'].lower().strip().split(' ')
    print(educational_organization, qualification)
    
    educational_organization = tfidfvectorizer_educational_organization.transform(educational_organization)
    qualification = tfidfvectorizer_qualification.transform(qualification)
    educational_organization = educational_organization.toarray()[0]
    qualification = qualification.toarray()[0]
    print(educational_organization, qualification)
    
    return jsonify({'message': 1}), 200
