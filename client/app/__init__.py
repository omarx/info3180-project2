from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from .config import Config
import os

app = Flask(__name__)

app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, '..', 'uploads')

from . import models
from .forms import UserForm, PostForm

from .models import Users, Posts, Likes, Follows, db
from . import views
