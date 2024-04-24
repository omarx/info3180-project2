from . import db
from datetime import datetime


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    firstname = db.Column(db.String(255))
    lastname = db.Column(db.String(255))
    location = db.Column(db.String(255))
    biography = db.Column(db.Text)
    profile_photo = db.Column(db.String(255))
    joined_on = db.Column(db.DateTime, default=datetime.utcnow)
