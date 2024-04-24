from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required
from .models import User
from . import db

auth = Blueprint('auth', __name__)


@auth.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    firstname = data.get('firstname')
    lastname = data.get('lastname')
    location = data.get('location')
    biography = data.get('biography')
    profile_photo = data.get('profile_photo')

    # Check if username or email already exists
    if User.query.filter_by(username=username).first() is not None:
        return jsonify({"message": "Username already taken"}), 409

    if User.query.filter_by(email=email).first() is not None:
        return jsonify({"message": "Email already registered"}), 409

    hashed_password = generate_password_hash(password)

    # Create a new user instance
    new_user = User(
        username=username,
        password=hashed_password,
        email=email,
        firstname=firstname,
        lastname=lastname,
        location=location,
        biography=biography,
        profile_photo=profile_photo
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201


@auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password, password):
        token = create_access_token(identity=username)
        return jsonify({"token": token}), 200
    return jsonify({"message": "Bad username or password"}), 401


