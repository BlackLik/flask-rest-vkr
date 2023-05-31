import pickle
from typing import Any, Literal
from flask import jsonify
from model import db, User
import requests


def get_ip() -> dict:
    req = requests.get('https://api.ipify.org/?format=json')
    return req.json()


def status_user(user_ip: str) -> tuple[str | None, Literal[200, 403, 404]]:
    user = User.query.filter_by(ip=user_ip).first()
    if user is None:
        return None, 404

    if user.status_user == 'blocked':
        return 'blocked', 403

    return user.status_user, 200


def check_user_params(data: dict):
    ip = ''
    if 'ip' not in data.keys():
        req = get_ip()
        ip = req['ip']
    else:
        ip = data['ip']
        if len(ip.split('.')) != 4 and any(i.isdigit() and 0 <= i <= 255 for i in ip.split('.')):
            return jsonify({'message': 'Bad request'}), 403

    _, code_status = status_user(ip)
    if code_status == 404:
        try:
            new_user = User(ip=ip, status_user='active')
            db.session.add(new_user)
            db.session.commit()
            code_status = 200
        except:
            db.session.rollback()
            return jsonify({'message': 'Bad request'}), 403

    if code_status != 200:
        return jsonify({'message': 'Bad request'}), code_status

    return None


def check_main_params(data: dict) -> (tuple[Any, Literal[400, 403, 404]] | None):
    if len(data.keys()) == 0:
        return jsonify({'message': 'Need parameters'}), 403

    if "gender" not in data.keys():
        return jsonify({'message': 'Bad request'}), 403

    if "region" not in data.keys():
        return jsonify({'message': 'Bad request'}), 403

    if 'educational_organization' not in data.keys():
        return jsonify({'message': 'Bad request'}), 403

    if 'qualification' not in data.keys():
        return jsonify({'message': 'Bad request'}), 403

    return None


def loader_model(path_model: str):
    with open(path_model, 'rb') as f:
        model = pickle.load(f)
    return model


def loader_tfidfvectorizer(name_model: str):
    model = loader_model(
        f"./models/tfidvectorizer/tfidfvectorizer_{name_model}.pkl"
    )
    return model
