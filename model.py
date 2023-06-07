from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


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


class Results(db.Model):
    __tablename__ = 'results'
    id = db.Column(db.Integer,
                   unique=True,
                   nullable=False,
                   primary_key=True,
                   autoincrement=True)
    id_user = db.Column(db.Integer,
                        db.ForeignKey('users.id'),
                        nullable=False)
    id_models_prediction = db.Column(db.Integer,
                                     db.ForeignKey('models_prediction.id'),
                                     nullable=False)
    id_form_of_education = db.Column(db.Integer,
                                     db.ForeignKey('form_of_education.id'),
                                     nullable=False)
    id_citizenship = db.Column(db.Integer,
                               db.ForeignKey('citizenship.id'),
                               nullable=False)
    id_profession_code = db.Column(db.Integer,
                                   db.ForeignKey('profession_code.id'),
                                   nullable=False)
    duration_of_education = db.Column(db.Integer,
                                      nullable=False)
    year_of_enrollment = db.Column(db.Integer,
                                   nullable=False)
    year_of_birth = db.Column(db.Integer,
                              nullable=False)
    disability = db.Column(db.Integer,
                           nullable=False)
    pension_for_childs_behalf = db.Column(db.Boolean,
                                          nullable=False,
                                          default=False)
    pension_for_childs = db.Column(db.Boolean,
                                   nullable=False,
                                   default=False)
    qualification = db.Column(db.Text,
                              nullable=False)
    educational_organization = db.Column(db.Text,
                                         nullable=False)
    predict = db.Column(db.Integer,
                        nullable=False,
                        default=0)
    probability_0 = db.Column(db.Float,
                              nullable=False,
                              default=1)
    probability_1 = db.Column(db.Float,
                              nullable=False,
                              default=0)

    datetime_create = db.Column(db.DateTime,
                                nullable=False,
                                default=datetime.utcnow)


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
    users_results = db.relationship('Results', backref='user', lazy=True)

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
    iso = db.Column(db.String(255), nullable=True)
    path_tag = db.Column(db.Text, nullable=True)
    region_model_prediction = db.relationship('ModelsPrediction',
                                              backref='region',
                                              lazy=True)

    def to_json(self):
        return {
            'id': self.id,
            'name_region': self.name_region,
            "iso": self.iso,
            "path_tag": self.path_tag
        }

    def get_all(self):
        return [region.to_json() for region in Regions.query.all()]

    def __repr__(self):
        return f'<Region {self.name_region}>'


class Citizenship(db.Model):
    __tablename__ = 'citizenship'
    id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
    name_citizenship = db.Column(db.String(255), nullable=False)
    citizenship_results = db.relationship(
        'Results', backref='citizenship', lazy=True)

    def to_json(self):
        return {
            'id': self.id,
            'name_citizenship': self.name_citizenship
        }

    def __repr__(self):
        return f'<Citizenship {self.name_citizenship}>'


class FormOfEducation(db.Model):
    __tablename__ = 'form_of_education'
    id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
    name_form_of_education = db.Column(db.String(255), nullable=False)
    form_of_education_results = db.relationship(
        'Results', backref='form_of_education', lazy=True)

    def to_json(self):
        return {
            'id': self.id,
            'name_form_of_education': self.name_form_of_education
        }

    def __repr__(self):
        return f'<FormOfEducation {self.name_form_of_education}>'


class ProfessionCode(db.Model):
    __tablename__ = 'profession_code'
    id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
    name_profession_code = db.Column(db.String(255), nullable=False)
    profession_code_results = db.relationship(
        'Results', backref='profession_code', lazy=True)

    def to_json(self):
        return {
            'id': self.id,
            'name_profession_code': self.name_profession_code
        }

    def __repr__(self):
        return f'<ProfessionCode {self.name_profession_code}>'
