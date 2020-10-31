from flask import Flask, request, jsonify, send_file
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from models import *
from exception import *
import datetime
from tokens import *
from queries import *

from __main__ import app, db




# {token : "string"}
@app.route('/updateUserData', methods=['POST'])
def updateUserData():
    try:
        if request.method != 'POST':
            raise InvalidUsage('Wrong request type', status_code=410)
        content = request.json
        user = getUserByToken(content["token"])
        profile = getProfileByToken(content["token"])
        user.update({
            'login' : content["login"],
            'password' : content["password"],
        })
        profile.update({
            'name' : content['name'],
            'last_name' : content['last_name'],
            'number' : content['number']
        })
        db.session.commit()

        print("after commit")
        return jsonify({'message' : 'data seccessfully updated'})
    except Exception as e:
        print(e)
        raise InvalidUsage("unable to update data", status_code=410)


#{token, new_data}
@app.route('/updateUserPhoto', methods=['POST'])
def updateUserPhoto():
    try:
        if request.method != 'POST':
            raise InvalidUsage('Wrong request type', status_code=410)

        file = request.files.get('photo')
        token = request.form.get('token')
        if 'photo' not in request.files:
            deleteProfilePhotoByToken(token)
            return jsonify({'message' : 'photo seccuessfully updated', 'photo' : ''})
        else:    
            filename = updateProfilePhotoByToken(token, file)
            if updateProfilePhotoByToken(token, file):
                return jsonify({'message' : 'photo seccuessfully updated!', 'photo' : "Uploads/Profiles/" + filename})
            else:
                raise InvalidUsage("photo update error", status_code=410)
    except Exception as e:
        print(e)
        raise e
