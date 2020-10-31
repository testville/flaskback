from flask import Flask, request, jsonify, url_for
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from models import *
from exception import *
import datetime
from tokens import *
from utils import *
import os

from __main__ import app, db, ALLOWED_EXTENSIONS, UPLOAD_FOLDER

def getAuthByToken(token):
    try:
        auth = Auth.query.filter(Auth.token == token)
        if(auth.count() != 1):
            raise InvalidUsage('unable to get profile via token', status_code=410)
        return auth
    except Exception as e:
        print(e)
        raise InvalidUsage('unable to get profile via token', status_code=410)

def getUserByToken(token):
    try:
        user_id = getAuthByToken(token).one().user_id
        user = Users.query.filter(Users.user_id == user_id)
        if(user.count() != 1):
            raise InvalidUsage('unable to get profile via token', status_code=410)
        return user
    except Exception as e:
        print(e)
        raise InvalidUsage('unable to get profile via token', status_code=410)

def getProfileByToken(token):
    try:
        user_id = getAuthByToken(token).one().user_id
        profile = Profiles.query.filter(Profiles.user_id == user_id)
        if(profile.count() != 1):
            raise InvalidUsage('unable to get profile via token', status_code=410)
        return profile
    except Exception as e:
        print(e)
        raise InvalidUsage('unable to get profile via token', status_code=410)

def getFullUserByToken(token):
    try:
        user = Users.query.join(Auth, Auth.user_id == Users.user_id)\
            .join(Profiles, Profiles.user_id == Users.user_id)\
            .filter(Auth.token == token)
        if(user.count() != 1):
            raise InvalidUsage('unable to get profile via token', status_code=410)
        return user
    except Exception as e:
        print(e)
        raise InvalidUsage('unable to get profile via token', status_code=410)

def deleteProfilePhotoByToken(token):
    try:
        profile = getProfileByToken(token)
        fileDelete(profile.one().photo, 'Profiles')
        profile.update({'photo' : ''})
        db.session.commit()
        return True
    except Exception as e:
        print(e)
        raise e

def addProfilePhotoByToken(token, file):
    try:
        filename = fileSave(file, 'Profiles')
        profile = getProfileByToken(token)
        profile.update({'photo' : filename})
        db.session.commit()
        return filename
    except Exception as e:
        print(e)
        raise e
    

def updateProfilePhotoByToken(token, file):
    try:
        deleteProfilePhotoByToken(token)
        filename = addProfilePhotoByToken(token, file)
        return filename
    except Exception as e:
        print(e)
        raise e


