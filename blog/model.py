from datetime import datetime

from blog import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
     return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    # _tablename_ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    bio = db.Column(db.String(100))
    avatar = db.Column(db.String(1014), default="../avatar/default.png")
    image_cover = db.Column(db.String(1014), default="../static/images/img.png")
    rank_id = db.Column(db.Integer, default=2) # except admin, rank_id=1
    user_rela = db.relationship('State', backref=db.backref('user', lazy=True))

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"


class State(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    is_author = db.Column(db.Boolean, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    comment = db.Column(db.Text)

    def __repr__(self):
        return (f"State('{self.is_author}', '{self.user_id}', '{self.post_id}')")


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False,  default=datetime.utcnow)
    title = db.Column(db.String(1014), nullable=False)
    content = db.Column(db.Text, nullable=False)
    image_cover = db.Column(db.String(1014), default="../static/images/img.png")
    post_rela = db.relationship('State', backref=db.backref('post', lazy=True))

    def __repr__(self):
        return f"Post('{self.title}', '{self.date}')"

