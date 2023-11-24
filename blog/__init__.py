from datetime import timedelta

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_ckeditor import CKEditor
from flask_login import LoginManager
from flask_mail import Mail
import os

app = Flask( __name__ )
app.config["SECRET_KEY"] = "r$qAjWhNN{GXD?x/ncd1xYd/t"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///blog.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.permanent_session_lifetime = timedelta(minutes=30)
app.app_context().push()

db = SQLAlchemy(app)
bcrypt = Bcrypt()
ckeditor = CKEditor(app)

login_manager = LoginManager(app)
login_manager.init_app(app)
login_manager.login_view = 'login'

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get("EMAIL")
app.config['MAIL_PASSWORD'] = os.environ.get("PASS")
mail = Mail(app)

from blog import route