from flask_sqlalchemy import SQLAlchemy
from enum import Enum
from datetime import datetime

db = SQLAlchemy()


class StatusUser(Enum):
    ACTIVE = 'active'
    BLOCKED = 'blocked'
    CHECKED = 'checked'


class ModelsPrediction(db.Model):
    __tablename__ = 'models_prediction'
    id = db.Column(db.Integer,
                   unique=True,
                   nullable=False,
                   primary_key=True,
                   autoincrement=True)
    name_model = db.Column(db.String(255), nullable=False)
    id_region = db.Column(db.Integer,
                          db.ForeignKey('regions.id'),
                          nullable=False)
    id_gender = db.Column(db.Integer,
                          db.ForeignKey('genders.id'),
                          nullable=False)
    path_scaller = db.Column(db.Text, nullable=False)
    path_model = db.Column(db.Text, nullable=False)

    def to_json(self):
        return {
            'id': self.id,
            'name_model': self.name_model,
            'id_region': self.id_region,
            'id_gender': self.id_gender,
            'path_scaller': self.path_scaller,
            'path_model': self.path_model
        }

    def __repr__(self):
        return f'<ModelsPrediction {self.id_region} {self.id_gender} {self.name_model}>'


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer,
                   nullable=False,
                   primary_key=True,
                   autoincrement=True)
    ip = db.Column(db.String(255), unique=True, nullable=True)
    status_user = db.Column(db.String(255), nullable=True)
    datetime_create = db.Column(db.DateTime,
                                default=datetime.utcnow,
                                nullable=False)

    def to_json(self):
        return {
            'id': self.id,
            'ip': self.ip,
            'status_user': self.status_user,
            'datetime_create': self.datetime_create
        }

    def __repr__(self):
        return f'<User {self.status_user} {self.ip}>'


class Genders(db.Model):
    __tablename__ = 'genders'
    id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
    name_gender = db.Column(db.String(255), nullable=False)
    gender_model_prediction = db.relationship('ModelsPrediction',
                                              backref='gender',
                                              lazy=True)

    def to_json(self):
        return {
            'id': self.id,
            'name_gender': self.name_gender
        }

    def get_all(self):
        return [gender.to_json() for gender in Genders.query.all()]

    def __repr__(self):
        return f'<Gender {self.name_gender}>'


class Regions(db.Model):
    __tablename__ = 'regions'
    id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
    name_region = db.Column(db.String(255), nullable=False)
    region_model_prediction = db.relationship('ModelsPrediction',
                                              backref='region',
                                              lazy=True)

    def to_json(self):
        return {
            'id': self.id,
            'name_region': self.name_region
        }

    def get_all(self):
        return [region.to_json() for region in Regions.query.all()]

    def __repr__(self):
        return f'<Region {self.name_region}>'
