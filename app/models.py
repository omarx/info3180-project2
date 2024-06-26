from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from . import db


class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password = db.Column(db.String(256))
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    email = db.Column(db.String(120), index=True, unique=True)
    location = db.Column(db.String(64))
    biography = db.Column(db.Text)
    profile_photo = db.Column(db.String(256))
    joined_on = db.Column(db.DateTime, nullable=False, default=datetime.now)

    # Relationships
    posts = db.relationship('Posts', backref='user', lazy='dynamic')
    likes = db.relationship('Likes', backref='user', lazy='dynamic')
    followed = db.relationship(
        'Follows',
        foreign_keys='Follows.follower_id',
        backref='follower',
        lazy='dynamic'
    )
    followers = db.relationship(
        'Follows',
        foreign_keys='Follows.followed_id',
        backref='followed',
        lazy='dynamic'
    )


class Posts(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    caption = db.Column(db.Text)
    photo = db.Column(db.String(128))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.now)


class Likes(db.Model):
    __tablename__ = 'likes'
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.now)


class Follows(db.Model):
    __tablename__ = 'follows'
    id = db.Column(db.Integer, primary_key=True)
    follower_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    followed_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.now)
