import os
from datetime import datetime
from flask_jwt_extended import create_access_token
from datetime import timedelta
from . import app
from flask import render_template, request, jsonify, send_from_directory
from flask_wtf import CSRFProtect
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from .forms import UserForm
from .models import db, Users

csrf = CSRFProtect(app)


@app.route('/api/v1/csrf-token/', methods=['GET'])
def get_csrf_token():
    from flask_wtf.csrf import generate_csrf
    return jsonify({'csrf_token': generate_csrf()})


@app.route('/')
def index():
    return jsonify(message="This is the beginning of our API")


@app.route('/api/v1/images/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/api/v1/auth/register', methods=['POST'])
def register():
    form = UserForm()
    if form.validate_on_submit():
        # Check if username or email already exists
        existing_user = Users.query.filter((Users.username == form.username.data) | (Users.email == form.email.data)).first()
        if existing_user:
            errors = []
            if existing_user.username == form.username.data:
                errors.append('Username is already taken.')
            if existing_user.email == form.email.data:
                errors.append('Email is already registered.')
            return jsonify({"errors": errors}), 409

        # Continue with registration if checks pass
        filename = None
        if form.profile_photo.data:
            filename = secure_filename(form.profile_photo.data.filename)
            form.profile_photo.data.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        user = Users(
            username=form.username.data,
            password_hash=generate_password_hash(form.password.data),
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data,
            location=form.location.data,
            biography=form.biography.data,
            profile_photo=filename,
            joined_on=datetime.now()
        )
        db.session.add(user)
        db.session.commit()

        return jsonify({
            "message": "User Successfully added",
            "username": user.username,
            "email": user.email
        }), 201
    else:
        return jsonify({"errors": form_errors(form)}), 400



@app.route('/api/v1/auth/login', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    if not username or not password:
        return jsonify({"msg": "Missing username or password"}), 400
    user = Users.query.filter_by(username=username).first()
    if user and check_password_hash(user.password_hash, password):
        access_token = create_access_token(identity=username, expires_delta=timedelta(days=1))
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({"msg": "Bad username or password"}), 401


###
# The functions below should be applicable to all Flask apps.
###

# Here we define a function to collect form errors from Flask-WTF
# which we can later use
def form_errors(form):
    error_messages = []
    """Collects form errors"""
    for field, errors in form.errors.items():
        for error in errors:
            message = u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            )
            error_messages.append(message)

    return error_messages


@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404
