from flask import render_template, flash, redirect, url_for, request

from blog import app, db
from blog.model import User, Post, State


@app.route('/')
@app.route('/index')
def index():
    pass


@app.route('/signup', methods=['GET', 'POST'])
def register():
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

@app.route('/reset_request', methods=['GET', 'POST'])
def reset_request():
    pass

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    pass