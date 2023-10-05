from flask import render_template, redirect, url_for, request, flash
from flask_login import current_user, login_user, logout_user, login_required

from blog import app, db, bcrypt
from blog.model import User, Post, State
from blog.form import SignupForm, LoginForm, UpdateAccountForm, PostForm


@app.route('/')
@app.route('/index')
def index():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date.desc()).paginate(page=page, per_page=5)
    return render_template('index.html', posts=posts)
    pass


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    pass

@app.route('/login', methods=['GET', 'POST'])
def login():
    pass

@app.route('/logout')
def logout():
    pass

@app.route('/account', methods=['GET', 'POST'])
def account():
    pass


@app.route('/post/new', methods=['GET', 'POST'])
def new_post():
    pass

@app.route('/post/<int:post_id>', methods=['GET', 'POST'])
def post(post_id):
    pass

@app.route('/post/<int:post_id>/update', methods=['GET', 'POST'])
def update_post(post_id):
    pass

@app.route('/post/<int:post_id>/delete', methods=['GET', 'POST'])
def delete_post(post_id):
    pass

# @app.route('/reset_request', methods=['GET', 'POST'])
# def reset_request():
#     pass

# @app.route('/reset_password/<token>', methods=['GET', 'POST'])
# def reset_password(token):
#     pass