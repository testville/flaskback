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
@app.route('/getTests', methods=['POST'])
def getTests():
    try:
        content = request.json
        returnList = {}
        returnList["tests"] = []
        Tests.query.all()
        for test in Tests.query.all():
            item = {}
            item["title"] = test.test_title
            item["description"] = test.test_description
            item["q_number"] = Questions.query.filter(Questions.test_id == test.test_id).count()
            if(Passes.query.filter(Passes.user_id == content["user_id"], Passes.test_id == test.test_id).count() == 0):
                item["passed"] = False
            else:
                item["passed"] = True
            lastPass = Passes.query.filter(Passes.user_id == content["user_id"], Passes.test_id == test.test_id).order_by(Passes.date.desc())
            if(lastPass.count() == 1):
                item["correct_answers"] = Answers.query.filter(Answers.pass_id == lastPass.one().pass_id, Answers.correctness == True).count()
            else:
                item["correct_answers"] = 0
            returnList["tests"].append(item)
        return jsonify(returnList)
    except Exception as e:
        print(e)
        raise InvalidUsage("unable to update data", status_code=410)

# {token : "string"}
@app.route('/getTest', methods=['POST'])
def getTest():
    try:
        content = request.json
        returnTest = {}
        t = Tests.query.filter(Tests.test_id == content["test_id"]).one()
        returnTest["title"] = t.test_title
        returnTest["description"] = t.test_description
        returnTest["questions"] = []
        for q in Questions.query.filter(Questions.test_id == content["test_id"]).all():
            item = {}
            item["q_id"] = q.q_id
            item["text"] = q.text
            item["type"] = q.q_type
            item["answers"] = q.answers_select
            returnTest["questions"].append(item)
        return jsonify(returnTest)
    except Exception as e:
        print(e)
        raise InvalidUsage("unable to update data", status_code=410)

# {user_id, test_id, answers[{q_id == q_id, type, answer = "" or []}]}
@app.route('/submitPass', methods=['POST'])
def submitPass():
    try:
        content = request.json
        _pass = Passes(user_id = content["user_id"], test_id = content["test_id"])
        if len(content["answers"]) != Tests.query.filter(Tests.test_id == content["test_id"]).join(Questions, Questions.test_id == content["test_id"]).count() :
            raise InvalidUsage("not enought answers", status_code=410)
        for a in content["answers"]:
            q = Questions.query.filter(Questions.q_id == a["q_id"]).one()
            _a = Answers(q_id = q.q_id)
            if a["type"] == "select":
                print("asd")
                _a.select_answers = a["answer"]
                _a.correctness = (set(q.correct_select) == set(a["answer"]))
            elif a["type"] == "write":
                _a.write_answer = a["answer"]
                _a.correctness = q.correct_write == a["answer"]
            _pass.answers.append(_a)
        db.session.add(_pass)
        db.session.commit()
        return jsonify({"message" : "Успешно добавлено"})
    except Exception as e:
        print(e)
        raise InvalidUsage("unable to update data", status_code=410)