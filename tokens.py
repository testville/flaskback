from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from models import *
from exception import *
import datetime
import random

from __main__ import app, db


def genToken():
    symbols_arr="ZYXWVUTSRQPONMLKJIHGFEDCBAzyxwvutsrqponmlkjihgfedcba1234567890"
    return ''.join([random.choice (symbols_arr) for i in range(50)])

def createToken(user):
    try:
        print(user.user_id)
        t = str(genToken())
        token = Auth(token = t, date = datetime.datetime.now(), user_id = user.user_id)
        print(token)
        Auth.query.filter(Auth.user_id == user.user_id).delete()
        db.session.add(token)
        db.session.commit()
        return t
    except Exception as e:
        print(e)
        raise InvalidUsage("Ошибка при создании уникального токена, повторите снова", status_code=410)


def validateToken(token):
    try:
        auth = Auth.query.filter(Auth.token == token)
        if((auth.date - datetime.datetime.now()).total_seconds() + 60 * 30 < 0):
                print((auth.date - datetime.datetime.now()).total_seconds() + 60 * 30)
                raise InvalidUsage("Токен устарел", status_code=410)
        else:
            updateToken(token)
            return true
    except expression as identifier:
        pass


def updateToken(token):
    try:
        Auth.query.filter(Auth.token == token).update({'date' : datetime.datetime.now()})
        db.session.commit()
    except Exception as e:
        print(e)
        raise InvalidUsage("Ошибка при обновлении токена", status_code=410)
