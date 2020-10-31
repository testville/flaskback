from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from models import *
from exception import *
import datetime
from tokens import *
from queries import *

from __main__ import app, db

# {token : token, name, last_name, login, password, number}
@app.route('/addUser', methods=['POST'])
def addUser():
    try:
        if request.method == 'POST':
                content = request.json
                profile = getFullUserByToken(content["token"]).all()[0]
                if(content["role"] != 'admin' and content["role"] != 'teacher' and content["role"] != 'student' ):
                    raise InvalidUsage("Нет такой роли", status_code=410)
                try:
                    if(profile.role != "admin"):
                        raise InvalidUsage('Недостаточные права пользователя. Производить добавление может только администратор', status_code=410)
                    checkIsUnique(content)
                    newUser = Users(login = content["login"], password = content["password"], role = content["role"])
                    newProfile = Profiles(name = content["name"], last_name = content["last_name"], number = content["number"])
                    newUser.profile = newProfile
                    db.session.add(newUser)
                    db.session.commit()
                    return jsonify({'message' : "Пользователь добавлен"})
                except InvalidUsage as e:
                    raise e
                except Exception as e:
                    print(e)
                    raise InvalidUsage("ошибка добавления пользователя", status_code=410)
        else:
            raise InvalidUsage('Wrong request type', status_code=410)
    except InvalidUsage as e:
        raise e 
    except Exception as e:
        print(e)
        raise InvalidUsage("Непредвиденная ошибка", status_code=410)

def checkIsUnique(inputData):
    if(len(Users.query.filter(Users.login == inputData["login"]).all()) != 0):
        raise InvalidUsage('Не уникальный логин', status_code=410)
        return False
    if(len(Profiles.query.filter(Profiles.number == inputData["number"]).all()) != 0):
        raise InvalidUsage('Не уникальный пароль', status_code=410)
        return False
    return True