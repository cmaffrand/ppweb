from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Prode(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    gameid = db.Column(db.Integer)
    team1goals = db.Column(db.Integer)
    team2goals = db.Column(db.Integer)
    teamadvance = db.Column(db.Integer, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
class Fixture(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    gameid = db.Column(db.Integer)
    group = db.Column(db.String(150))
    team1 = db.Column(db.String(150))
    team2 = db.Column(db.String(150))    
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    notes = db.relationship('Note')
    prodes = db.relationship('Prode')
    fixtures = db.relationship('Fixture')
    
    
