from flask_sqlalchemy import SQLAlchemy
import datetime
db = SQLAlchemy()

class Users(db.Model):
    user_id = db.Column(db.BigInteger, primary_key=True, unique=True)
    push_key = db.Column(db.String(255), nullable=True)
    role = db.Column(db.String(255), unique=False, nullable=False)
    login = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), unique=False, nullable=False)
    auth = db.relationship('Auth', backref='users', lazy=True, uselist=False)
    profile = db.relationship('Profiles', backref='users', lazy=True, uselist=False)
    achivments = db.relationship('Achivments', backref='users', lazy=True, uselist=False)

    def __repr__(self):
        return '<user_id {}> <push_key {}> <role {}> <login{}> <password{}> <profile {}> <auth {}>'.format(self.user_id, self.push_key, self.role, self.login, self.password, self.profile, self.auth)

class Auth(db.Model):
    user_id = db.Column(db.BigInteger, db.ForeignKey('users.user_id'), primary_key=True)
    token = db.Column(db.String(255), nullable=False, unique=True)
    date = db.Column(db.DateTime, unique=False, nullable=False)

    def __repr__(self):
        return '<user_id {}> <push_key {}> <role {}>'.format(self.user_id, self.token, self.date)

class Profiles(db.Model):
    user_id = db.Column(db.BigInteger, db.ForeignKey('users.user_id'), unique=True, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=False)
    last_name = db.Column(db.String(255), nullable=False, unique=False)
    photo = db.Column(db.String(255), zero_indexes=True, default="")
    number = db.Column(db.String(255), unique=True, nullable=False)

    def __repr__(self):
        return '<user_id {}> <name {}> <last_name {}> <photo {}> <number {}>'.format(self.user_id, self.name, self.last_name, self.photo, self.number)

class Achivments(db.Model):
    a_id = db.Column(db.BigInteger, primary_key=True, unique=True)
    user_id = db.Column(db.BigInteger, db.ForeignKey('users.user_id'))
    date = db.Column(db.DateTime, nullable=False, unique=False)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    photos = db.Column(db.ARRAY(db.String(255)), zero_indexes=True)

    def __repr__(self):
        return '<a_id {}> <user_id {}> <date {}> <title {}> <photos {}>'.format(self.a_id, self.user_id, self.date, self.title, self.photos)

class Tests(db.Model):
    test_id = db.Column(db.BigInteger, primary_key=True, unique=True)
    test_title = db.Column(db.String(255), nullable=False, unique=False)
    test_description = db.Column(db.Text, nullable=False, unique=False)
    
    questions = db.relationship('Questions', backref='tests', lazy=True, uselist=True)
    passes = db.relationship('Passes', backref='tests', lazy=True, uselist=True)
    def __repr__(self):
        return 'Tests'

class Questions(db.Model):
    q_id = db.Column(db.BigInteger, primary_key=True, unique=True)
    test_id = db.Column(db.BigInteger, db.ForeignKey('tests.test_id'))
    text = db.Column(db.Text, nullable=False, unique=False)
    q_type = db.Column(db.String(255), nullable=False)
    answers_select = db.Column(db.ARRAY(db.Text), zero_indexes=True, nullable=True, unique=False) 
    correct_write = db.Column(db.Text, zero_indexes=True, nullable=True, unique=False) 
    correct_select = db.Column(db.ARRAY(db.Integer), zero_indexes=True, nullable=True, unique=False) 

    answers = db.relationship('Answers', backref='questions', lazy=True, uselist=True)
    def __repr__(self):
        return 'Questions'

class Passes(db.Model):
    pass_id = db.Column(db.BigInteger, primary_key=True, unique=True)
    user_id = db.Column(db.BigInteger, db.ForeignKey('users.user_id'))
    test_id = db.Column(db.BigInteger, db.ForeignKey('tests.test_id'))
    date = db.Column(db.Date, nullable=False, default=datetime.datetime.now)

    answers = db.relationship('Answers', backref='passes', lazy=True, uselist=True)
    def __repr__(self):
        return 'Passes'

class Answers(db.Model):
    answer_id = db.Column(db.BigInteger, primary_key=True, unique=True)
    q_id = db.Column(db.BigInteger, db.ForeignKey('questions.q_id'))
    pass_id = db.Column(db.BigInteger, db.ForeignKey('passes.pass_id'))
    write_answer = db.Column(db.Text, zero_indexes=True, nullable=True, unique=False, default="")
    select_answers = db.Column(db.ARRAY(db.Integer), zero_indexes=True, nullable=True, unique=False, default=[]) 
    correctness = db.Column(db.Boolean, zero_indexes=True, nullable=False, unique=False)
    def __repr__(self):
        return 'Answers'