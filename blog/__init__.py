from datetime import timedelta

from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(  __name__ )
app.config["SECRET_KEY"] = "my-secret-key"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///blog.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.permanent_session_lifetime = timedelta(minutes=1)
app.app_context().push()
db = SQLAlchemy(app)

from blog import route