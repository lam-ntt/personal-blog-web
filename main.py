from flask import Flask, redirect, url_for, render_template, request, session
from datetime import timedelta
from flask.helpers import flash
from flask_sqlalchemy import SQLAlchemy
from os import path
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(  __name__ )
app.config["SECRET_KEY"] = "my-secret-key"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///user.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.permanent_session_lifetime = timedelta(minutes=1)

db = SQLAlchemy(app)


class User(db.Model):
    # _tablename_ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False)
    user_name = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(300), nullable=False)
    bio = db.Column(db.String(100))
    avatar = db.Column(db.String(1014))
    image_cover = db.Column(db.String(1014))
    rank_id = db.Column(db.Integer)
    user_rela = db.relationship('States', backref=db.backref('user', lazy=True))

    def __init__(self, user_name, email, password, bio, avatar="../avatar/default.png", rank_id=2, image_cover="../static/images/img.png"):
        self.user_name = user_name
        self.email = email
        self.password = generate_password_hash(password)
        self.bio = bio
        self.avatar = avatar
        self.rank_id = rank_id
        self.image_cover = image_cover

    def check_password(self, password_hash):
        return check_password_hash(self.password, password_hash)


class States(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    is_author = db.Column(db.Boolean, nullable=False)
    blog_id = db.Column(db.Integer, db.ForeignKey('blog_post.id'))
    comment = db.Column(db.Text)


class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image_cover = db.Column(db.String(1014))
    date = db.Column(db.DateTime, nullable=False)
    title = db.Column(db.String(1014), nullable=False)
    subtitle = db.Column(db.String(1014))
    body = db.Column(db.Text, nullable=False)
    BlogPost_rela = db.relationship('States', backref=db.backref('BlogPost', lazy=True))


@app.route('/select/user')
def select():
    # data_user = User.query.filter_by(user_name='chuong').first()
    users = User.query.all()
    html = '';
    for user in users:
        html = html + "<br>" + user.user_name;

    return html


# @app.route('/insert', methods=["GET"])
def insert_test():
    new_user = User('Admin', 'admin@gmail.com', '12345678', 'Admin');
    db.session.add(new_user)
    db.session.commit()
    return 'Da insert du lieu'


def check_pass():
    user = User.query.filter_by(user_name='username1').first()
    if user:
        if user.check_password('12345678') == True:
            return "mat khau dung"
        else:
            return 'sai'
    else:
        return 'khong co username như v'


with app.app_context():
    if not path.exists("user.db"):
        db.create_all()
        insert_test()
        print("Created database!")
