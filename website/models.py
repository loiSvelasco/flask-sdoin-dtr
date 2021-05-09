from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64))
    password = db.Column(db.String(64))

class DailyTimeRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time_in_am = db.Column(db.DateTime(timezone=True))
    time_out_am = db.Column(db.DateTime(timezone=True))
    time_in_pm = db.Column(db.DateTime(timezone=True))
    time_out_pm = db.Column(db.DateTime(timezone=True))
    staff_id = db.Column(db.Integer, db.ForeignKey('staff.id'))

class Staff(db.Model):
    id = db.Column(db.Integer, primary_key=True) 
    staff_id_no = db.Column(db.String(64), unique=True)
    name = db.Column(db.String(128))
    position = db.Column(db.String(64))
    gender = db.Column(db.String(10))
    address = db.Column(db.String(128))
    dtr = db.relationship('DailyTimeRecord')

    

