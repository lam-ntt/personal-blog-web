from datetime import timedelta

from flask import Flask
from flask_ckeditor import CKEditor
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail


app = Flask( __name__ )
ckeditor = CKEditor(app)
app.config["SECRET_KEY"] = "r$qAjWhNN{GXD?x/ncd1xYd/t"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///blog.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.permanent_session_lifetime = timedelta(minutes=1)
app.app_context().push()

db = SQLAlchemy(app)
bcrypt = Bcrypt()

login_manager = LoginManager(app)
login_manager.login_view = 'login'

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'nguyenthithanhlam2017@gmail.com'
app.config['MAIL_PASSWORD'] = 'ecif ztdk lukn jaye'
mail = Mail(app)

from blog import route