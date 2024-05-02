from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, TextAreaField, SelectField, IntegerField, DecimalField
from wtforms.fields.simple import PasswordField
from wtforms.validators import InputRequired, NumberRange, Email


class UserForm(FlaskForm):
    username = StringField('Title', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    first_name = StringField('First Name', validators=[InputRequired()])
    last_name = StringField('Last Name', validators=[InputRequired()])
    email = StringField('Email', validators=[InputRequired(), Email()])
    location = StringField('Location', validators=[InputRequired()])
    biography = TextAreaField('Biography', validators=[InputRequired()])
    profile_photo = StringField('Profile Photo', validators=[InputRequired()])


class PostForm(FlaskForm):
    caption = StringField('Title', validators=[InputRequired()])
    photo = FileField('Photo', validators=[FileAllowed(['jpg', 'png'])])
    user_id = StringField('User ID', validators=[InputRequired()])
