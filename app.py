import pickle
from flask import Flask, jsonify, request
from api import api
from flask_cors import CORS
from model import db
import config

app = Flask(__name__)
app.register_blueprint(api, url_prefix='/api')
app.config['SQLALCHEMY_DATABASE_URI'] = config.db_url_connection
db.init_app(app)
CORS(app)


if __name__ == '__main__':
    app.run(debug=config.debug, host=config.flask_host, port=5000)
