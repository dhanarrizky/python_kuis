from . import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    nickname = db.Column(db.String(255))
    skor = db.relationship('SkorUser')


class SkorUser(db.Model):
    __tablename__ = 'skor'
    id = db.Column(db.Integer, primary_key=True)
    idUser = db.Column(db.Integer, db.ForeignKey('user.id'))
    skor = db.Column(db.Integer)


class Question(db.Model):
    __tablename__ = 'question'
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String)
    answer = db.Column(db.String(255))
    option1 = db.Column(db.String(255))
    option2 = db.Column(db.String(255))
    option3 = db.Column(db.String(255))
    option4 = db.Column(db.String(255))