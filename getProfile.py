from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from models import *
from exception import *
import datetime
from tokens import *
from queries import *

from __main__ import app, db

# {token : "string"}
@app.route('/getProfile', methods=['POST'])
def getProfile():
    try:
        content = request.json
        user = getFullUserByToken(content["token"]).all()[0]
        print(user)
        return jsonify({
            "token" : user.auth.token,
            "login" : user.login,
            "password" : user.password,
            "name" : user.profile.name,
            "last_name" : user.profile.last_name,
            "photo" : user.profile.photo,
            "number" : user.profile.number
        })
    except InvalidUsage as e:
        print(e)
        raise e
    except Exception as e:
        print(e)
        raise InvalidUsage("get profile error", status_code=410)
