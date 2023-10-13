from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError

from flask_login import current_user
from blog.model import User


class SignupForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired(), Length(min=2)])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Signup')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('This email is taken. Please choose a difference one.')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('This username is taken. Please choose a difference one.')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    bio = StringField('Biography')
    avatar = FileField('Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    image_cover = FileField('Cover Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            if user.email == current_user.email: return
            else: raise ValidationError('This email is taken. Please choose a difference one.')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            if user.username == current_user.username: return
            else: raise ValidationError('This username is taken. Please choose a difference one.')

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    image_cover = FileField('Cover Picture', validators=[DataRequired()])
    submit = SubmitField('Post')

class CommentForm(FlaskForm):
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')
    
class RequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            if user.email == current_user.email: return
            else: raise ValidationError('This email is not linked to any account. Please register first')

class ResetForm(FlaskForm):
    password = StringField('Password', validators=[DataRequired()])
    confirm_password = StringField('Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Signup')






