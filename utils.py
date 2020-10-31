from flask import Flask, request, jsonify, url_for
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from models import *
from exception import *
import datetime
from queries import *
import os

from __main__ import app, db, ALLOWED_EXTENSIONS, UPLOAD_FOLDER

def allowedFile(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def fileSearch(filename, folder_name):
    filename = secure_filename(filename)
    return os.path.isfile(os.path.join(app.config['UPLOAD_FOLDER'], folder_name, filename)) 

def fileDelete(filename, folder_name):
    try:
        filename = secure_filename(filename)
        Profiles.query.filter(Profiles.photo == filename).update({'photo' : ''})
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], folder_name, filename)
        if(os.path.isfile(file_path) ):
            os.remove(file_path)
        db.session.commit()
        return True
    except Exception as e:
        print(e)
        raise e
    

def fileSave(file, folder_name):
    try:
        if file and allowedFile(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], folder_name, filename))
            return filename
    except Exception as e:
        print(e)
        raise e
    