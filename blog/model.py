from datetime import datetime

from blog import db


class User(db.Model):
    # _tablename_ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    bio = db.Column(db.String(100))
    avatar = db.Column(db.String(1014), default="../avatar/default.png")
    image_cover = db.Column(db.String(1014), default="../static/images/img.png")
    rank_id = db.Column(db.Integer, default=2)
    user_rela = db.relationship('State', backref=db.backref('user', lazy=True))

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.avatar}')"


class State(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    is_author = db.Column(db.Boolean, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    blog_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    comment = db.Column(db.Text)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False,  default=datetime.utcnow)
    title = db.Column(db.String(1014), nullable=False)
    content = db.Column(db.Text, nullable=False)
    image_cover = db.Column(db.String(1014), default="../static/images/img.png")
    post_rela = db.relationship('State', backref=db.backref('post', lazy=True))

    def __repr__(self):
        return f"Post('{self.title}', '{self.date}')"

