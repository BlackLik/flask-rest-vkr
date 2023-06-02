import pickle
from flask import Blueprint, request, jsonify
import function as fn
from model import db, User, Regions, Genders, ModelsPrediction, Results, Citizenship, FormOfEducation, ProfessionCode
from functools import wraps
import requests
import numpy as np


api = Blueprint('api', __name__, url_prefix='/api')
tfidfvectorizer_educational_organization = fn.loader_tfidfvectorizer(
    'educational_organization')
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

@api.route('/profession_codes', methods=['GET'])
def profession_codes():
    profession_codes = ProfessionCode.query.all()
    return jsonify({'profession_codes': [profession_code.to_json() for profession_code in profession_codes]}), 200

@api.route('/profession_codes/<int:profession_code_id>', methods=['GET'])
def profession_code(profession_code_id):
    prof = ProfessionCode.query.filter_by(id=profession_code_id).first()
    return jsonify({'profession_code': prof.to_json()}), 200

@api.route('/form_of_educations', methods=['GET'])
def form_of_educations():
    form_of_educations = FormOfEducation.query.all()
    return jsonify({'form_of_educations': [form_of_education.to_json() for form_of_education in form_of_educations]}), 200

@api.route('/form_of_educations/<int:form_of_education_id>', methods=['GET'])
def form_of_education(form_of_education_id):
    form_of_education = FormOfEducation.query.filter_by(id=form_of_education_id).first()
    return jsonify({'form_of_education': form_of_education.to_json()}), 200

@api.route('/citizenships', methods=['GET'])
def citizenships():
    citizenships = Citizenship.query.all()
    return jsonify({'citizenships': [citizenship.to_json() for citizenship in citizenships]}), 200

@api.route('/citizenships/<int:citizenship_id>', methods=['GET'])
def citizenship(citizenship_id):
    citizenship = Citizenship.query.filter_by(id=citizenship_id).first()
    return jsonify({'citizenship': citizenship.to_json()}), 200


@api.route('/predict', methods=['POST'])
@login_required
def predict():
    data = request.json
    result = fn.check_main_params(data=data)
    if result is not None:
        return result

    model_object = ModelsPrediction.query.filter_by(
        id_region=data['region'], id_gender=data['gender']).first()
    if model_object is None:
        return jsonify({'message': 'Model not found'}), 404

    educational_organization = data['educational_organization'].lower(
    ).strip().split(' ')
    qualification = data['qualification'].lower().strip().split(' ')
    educational_organization = tfidfvectorizer_educational_organization.transform(
        educational_organization)
    qualification = tfidfvectorizer_qualification.transform(qualification)
    educational_organization = educational_organization.toarray()[0]
    qualification = qualification.toarray()[0]

    try:
        X = np.array([
            data['form_of_education'],
            data['profession_code'],
            data['duration_of_education'],
            data['year_of_enrollment'],
            data['citizenship'],
            data['year_of_birth'],
            data['disability'],
            data['pension_for_childs_behalf'],
            data['pension_for_childs'],
            *educational_organization[0:2],
            *qualification
        ]).reshape(1, -1)

        scaller = fn.loader_model('./'+model_object.path_scaller)
        model_predict = fn.loader_model('./'+model_object.path_model)
        X_scaller = scaller.transform(X)
        y_predict = model_predict.predict(X_scaller)
        y_proba = model_predict.predict_proba(X_scaller)
        

        try:
            user = User.query.filter_by(ip=data['ip']).first()
            new_result = Results(
                id_user=int(user.id),
                predict=int(y_predict),
                probability_0=float(y_proba[0][0]),
                probability_1=float(y_proba[0][1]),
                id_models_prediction=int(model_object.id),
                id_form_of_education=int(data['form_of_education']),
                id_citizenship=int(data['citizenship']),
                id_profession_code=int(data['profession_code']),
                duration_of_education=int(data['duration_of_education']),
                year_of_enrollment=int(data['year_of_enrollment']),
                year_of_birth=int(data['year_of_birth']),
                disability=int(data['disability']),
                pension_for_childs_behalf=bool(data['pension_for_childs_behalf']),
                pension_for_childs=bool(data['pension_for_childs']),
                educational_organization=str(data['educational_organization']),
                qualification=str(data['qualification'])
            )
            db.session.add(new_result)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(e)
            return jsonify({'message': e}), 500

        return jsonify({'message': {"prediction": int(y_predict), "probability": [float(y_proba[0][0]), float(y_proba[0][1])]}}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500
