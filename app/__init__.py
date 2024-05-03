from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from .config import Config
import os
from dotenv import load_dotenv

load_dotenv()

from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.config.from_object(Config)
app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, '..', 'uploads')
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY')

db = SQLAlchemy(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)

from . import models, views
from .forms import UserForm, PostForm
from .models import Users, Posts, Likes, Follows, db
