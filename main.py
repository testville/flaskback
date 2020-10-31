from flask import Flask, request, jsonify, send_from_directory, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models import *
from exception import *
import datetime
import random
import os
from sqlalchemy.exc import IntegrityError

UPLOAD_FOLDER = "/home/ubuntu/talent/Uploads"

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://admin:123@130.193.49.130:5432/talent"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#db = SQLAlchemy(app)
#migrate = Migrate(app, db)
db.app = app
db.init_app(app)
db.create_all()
db.session.commit()

from tokens import *
import getProfile
import auth
import addUser  
import updateUserData
from updateUserData import updateUserData, updateUserPhoto
from tests import *
@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

@app.route('/Uploads/<folder>/<image>')
def send_image(folder, image):
    return send_file(os.path.join(app.config['UPLOAD_FOLDER'], folder, image), mimetype='image/gif')

@app.route('/')
def hello_world():
    return "1"

    

if __name__ == '__main__':
    app.run(host= '0.0.0.0')
    
    