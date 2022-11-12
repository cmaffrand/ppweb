from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Prode(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    gameid = db.Column(db.Integer)
    team1goals = db.Column(db.Integer)
    team2goals = db.Column(db.Integer)
    teamadvance = db.Column(db.Integer, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Fixture(db.Model):
    gameid = db.Column(db.Integer, primary_key=True)
    stage = db.Column(db.String(150))
    team1 = db.Column(db.String(150))
    team2 = db.Column(db.String(150))
    date = db.Column(db.DateTime(timezone=True), default=func.now())

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    score = db.Column(db.Integer, default=0)
    prodes = db.relationship('Prode')
    
class Results(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    team1goals = db.Column(db.Integer)
    team2goals = db.Column(db.Integer)
    state = db.Column(db.String(150))
    
class Linkgames(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    link = db.Column(db.String(1000))
