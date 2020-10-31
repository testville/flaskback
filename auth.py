from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from models import *
from exception import *
import datetime
from tokens import *


from __main__ import app, db


# {token : token, name, last_name, login, password, number}
@app.route('/auth', methods=['POST'])
def auth():
    if request.method == 'POST':
        try:
            content = request.json
            print(content)
            query = Users.query.filter(Users.login == content["login"] and Users.password == content["password"]).all()
            if(len(query) == 1):
                token = createToken(query[0])
                return jsonify({"token" : token})
            else:
                raise InvalidUsage("Неправильное сочетание логин/пароль", status_code=410)  
        except InvalidUsage as e:
            raise e
        except Exception as e:
            print(e)
            raise e
    else:
        raise InvalidUsage('Wrong request type', status_code=410)