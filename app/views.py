import os
from sqlalchemy import func
from datetime import datetime
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta
from . import app
from flask import render_template, request, jsonify, send_from_directory
from flask_wtf import CSRFProtect
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from .forms import UserForm, PostForm
from .models import db, Users, Posts, Likes, Follows

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
        existing_user = Users.query.filter(
            (Users.username == form.username.data) | (Users.email == form.email.data)).first()
        if existing_user:
            errors = []
            if existing_user.username == form.username.data:
                errors.append('Username is already taken.')
            if existing_user.email == form.email.data:
                errors.append('Email is already registered.')
            return jsonify({"errors": errors}), 409
        filename = None
        if form.profile_photo.data:
            filename = secure_filename(form.profile_photo.data.filename)
            form.profile_photo.data.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        user = Users(
            username=form.username.data,
            password=generate_password_hash(form.password.data),
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
    if user and check_password_hash(user.password, password):
        access_token = create_access_token(identity={"username": username, "user_id": user.id},
                                           expires_delta=timedelta(days=10))
        return jsonify(access_token=access_token, user_id=user.id), 200
    else:
        return jsonify({"msg": "Bad username or password"}), 401


@app.route('/api/v1/users/<int:user_id>/posts', methods=['POST'])
@jwt_required()
def new_post(user_id):
    form = PostForm()
    if form.validate_on_submit():
        filename = None
        if form.photo.data:
            filename = secure_filename(form.photo.data.filename)
            form.photo.data.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        post = Posts(
            caption=form.caption.data,
            photo=filename,
            user_id=user_id,
        )
        db.session.add(post)
        db.session.commit()
        return jsonify({"message": "Post created"}), 201

    else:
        return jsonify({"errors": form_errors(form)}), 400


@app.route('/api/v1/users/<int:user_id>/posts/', methods=['GET'])
@jwt_required()
def get_user_posts(user_id):
    posts = Posts.query.filter_by(user_id=user_id).all()
    if posts:
        posts_data = [{
            "post_id": post.id,
            "caption": post.caption,
            "photo": post.photo,
            "created_at": post.created_at.strftime('%Y-%m-%d %H:%M:%S')
        } for post in posts]
        return jsonify(posts_data), 200
    else:
        return jsonify({"message": "No posts found for this user"}), 404


@app.route('/api/v1/posts', methods=['GET'])
@jwt_required()
def get_posts():
    # Query posts along with associated user info and likes count
    posts = db.session.query(
        Posts.id,
        Posts.caption,
        Posts.photo,
        Posts.created_at,
        Users.username,
        Users.profile_photo,
        Users.id.label('user_id'),
        func.count(Likes.id).label('likes_count')
    ).select_from(Posts
                  ).join(Users
                         ).outerjoin(Likes, Likes.post_id == Posts.id
                                     ).group_by(Posts.id, Users.id
                                                ).all()

    posts_list = [{
        "caption": post.caption,
        "photo": post.photo,
        "username": post.username,
        "profile_photo": post.profile_photo,
        "user_id": post.user_id,
        "likes_count": post.likes_count,
        "created_at": post.created_at.strftime('%Y-%m-%d %H:%M:%S')
    } for post in posts]

    return jsonify(posts_list), 200


@app.route('/api/v1/user/<int:user_id>', methods=['GET'])
def get_user_profile(user_id):
    user = db.session.query(
        Users.id,
        Users.first_name,
        Users.last_name,
        Users.profile_photo,
        Users.biography,
        Users.joined_on,
        Users.location,
        db.func.count(Posts.id).label('posts_count'),
        db.func.count(Follows.follower_id.distinct()).label('follower_count')
    ).outerjoin(Posts, Posts.user_id == Users.id
                ).outerjoin(Follows, Follows.followed_id == Users.id
                            ).filter(Users.id == user_id
                                     ).group_by(Users.id).first()

    if not user:
        return jsonify({'message': 'User not found'}), 404

    follower_ids = db.session.query(Follows.follower_id).filter(Follows.followed_id == user_id).all()
    follower_ids_list = [f.follower_id for f in follower_ids]  #

    response = {
        'user_id': user.id,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'profile_photo': user.profile_photo,
        'biography': user.biography,
        'joined_on': user.joined_on.strftime('%Y-%m-%d'),
        'location': user.location,
        'posts_count': user.posts_count,
        'follower_count': user.follower_count,
        'followers_ids': follower_ids_list
    }
    return jsonify(response), 200


@app.route('/api/v1/posts/<int:post_id>/like', methods=['POST'])
@jwt_required()
def like_post(post_id):
    identity = get_jwt_identity()
    user_id = identity['user_id']

    post = db.session.query(Posts).filter(Posts.id == post_id).first()
    if not post:
        return jsonify({'message': 'Post not found'}), 404

    existing_like = db.session.query(Likes).filter_by(post_id=post_id, user_id=user_id).first()
    if existing_like:
        return jsonify({'message': 'You have already liked this post'}), 409

    new_like = Likes(
        post_id=post_id,
        user_id=user_id,
        created_at=datetime.now()
    )
    db.session.add(new_like)
    db.session.commit()

    return jsonify({'message': 'Like added'}), 201


@app.route('/api/v1/users/<int:followed_id>/follow', methods=['POST'])
@jwt_required()
def follow_user(followed_id):
    identity = get_jwt_identity()
    follower_id = identity['user_id']
    if follower_id == followed_id:
        return jsonify({"msg": "Users cannot follow themselves"}), 400
    existing_follow = db.session.query(Follows).filter_by(follower_id=follower_id, followed_id=followed_id).first()
    if existing_follow:
        return jsonify({"msg": "Already following this user"}), 409
    new_follow = Follows(
        follower_id=follower_id,
        followed_id=followed_id,
        created_at=datetime.now()
    )
    db.session.add(new_follow)
    db.session.commit()

    return jsonify({"message": "Follow successful"}), 201


# Note: Consider adding error handling for scenarios where either user does not exist.

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
