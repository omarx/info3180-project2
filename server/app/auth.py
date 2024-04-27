from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask_jwt_extended import create_access_token, jwt_required
from .models import User
from . import db
import os
from flask import current_app
import uuid
from datetime import datetime

auth = Blueprint('auth', __name__)


def save_uploaded_file(file):
    if file:
        filename = secure_filename(file.filename)
        _, file_extension = os.path.splitext(filename)
        random_name = str(uuid.uuid4())
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        new_filename = f"{random_name}_{timestamp}{file_extension}"
        project_root = os.path.join(current_app.root_path, '..')
        file_path = os.path.join(project_root, 'static', 'photo', 'profile_pics', new_filename)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        file.save(file_path)
        return new_filename
    return None


@auth.route('/register', methods=['POST'])
def register():
    try:
        if request.is_json:
            data = request.get_json()
            username = data.get('username')
            password = data.get('password')
            email = data.get('email')
            firstname = data.get('firstname')
            lastname = data.get('lastname')
            location = data.get('location')
            biography = data.get('biography')
            profile_photo = request.files.get('profile_photo')
        else:
            username = request.form['username']
            password = request.form['password']
            email = request.form['email']
            firstname = request.form['firstname']
            lastname = request.form['lastname']
            location = request.form['location']
            biography = request.form['biography']
            profile_photo = request.files.get('profile_photo')

        photo_filename = save_uploaded_file(profile_photo) if profile_photo else None

        if User.query.filter((User.username == username) | (User.email == email)).first():
            response = jsonify({"error": "Username or email already registered"})
            print("Response:")
            print(response)  # Print the response
            return response, 409

        hashed_password = generate_password_hash(password)
        new_user = User(
            username=username,
            password=hashed_password,
            email=email,
            firstname=firstname,
            lastname=lastname,
            location=location,
            biography=biography,
            profile_photo=photo_filename,
        )
        db.session.add(new_user)
        db.session.commit()

        response = jsonify({"message": "User registered successfully"})
        print("Response:")
        print(response)  # Print the response
        return response, 201
    except Exception as e:
        response = jsonify({"error": str(e)})
        print("Response:", e)
        print(response)  # Print the response
        return response, 500


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
