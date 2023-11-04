import os, secrets # image processing

from flask import render_template, redirect, url_for, request, flash, abort
from flask_login import current_user, login_user, logout_user, login_required
from flask_mail import Message
from functools import wraps

from blog import app, db, bcrypt, mail
from blog.model import User, Post, State
from blog.form import SignupForm, LoginForm, UpdateAccountForm, PostForm, CommentForm, RequestForm, ResetForm


#Create admin-only decorator
def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.rank_id != 1:
            return render_template('forbidden.html')
        return f(*args, **kwargs)
    return decorated_function

def owner_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        post_id = request.args.get('post_id')
        author_state = State.query.filter_by(is_author=True, post_id=post_id).first()
        if current_user.id != author_state.user_id:
            return render_template('forbidden.html')
        return f(*args, **kwargs)
    return decorated_function

def get_author(post):
    state = State.query.filter_by(is_author=True, post_id=post.id).first()
    if state==None: #just for window
        author = User.query.filter_by(id=1).first()
    else:
        author = User.query.filter_by(id=state.user_id).first()
    if author==None: author=User.query.first() #just for window
    return author


@app.route('/')
@app.route('/home')
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date.desc()).paginate(page=page,
                                                           per_page=3)
    return render_template('index.html', posts=posts)

@app.route('/admin')
@login_required
@admin_only
def admin():
    posts = Post.query.order_by(Post.date.desc()).all()
    authors = []
    for post in posts:
        authors.append(get_author(post))
    return render_template('admin_account.html', posts=posts, authors=authors)



@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        hash_password = bcrypt.generate_password_hash(form.password.data)
        user = User(email=form.email.data, username=form.username.data, password=hash_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created. You are now able to login.',
              'success')
        return redirect(url_for('login'))
    else:
        if form.is_submitted():
            flash('Your mail or username is invalid!', 'danger')
    return render_template('sign_up.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash('You logged in fail. Please check the email and password!', 'danger')
            redirect(url_for('login'))
    return render_template('log_in.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/', picture_fn)
    form_picture.save(picture_path)
    picture_fn = '..\static\\' + picture_fn
    return picture_fn

@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    posts_state = State.query.filter_by(is_author=True, user_id=current_user.id)
    posts = []
    for state in posts_state:
        posts.append(Post.query.filter_by(id=state.post_id).first())
    return render_template('account.html', posts=posts)

@app.route('/account/update', methods=['GET', 'POST'])
@login_required
def update_account():
    form = UpdateAccountForm(
        username=current_user.username,
        bio=current_user.bio,
        image_cover=current_user.image_cover
    )
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.bio = form.bio.data
        if form.avatar.data:
            print(form.avatar.data)
            current_user.avatar = save_picture(form.avatar.data)
        if form.image_cover.data:
            current_user.image_cover = form.image_cover.data
        db.session.commit()
        flash('Your account info has been updated!', 'success')
        return redirect(url_for('account'))
    return render_template('update_account.html', form=form)



@app.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data,
                    image_cover=form.image_cover.data)
        db.session.add(post)
        db.session.commit()

        post = Post.query.order_by(Post.id.desc()).first()
        state = State(is_author=True, user_id=current_user.id, post_id=post.id)
        db.session.add(state)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('new_post.html', form=form)


@app.route('/post/<int:post_id>', methods=['GET', 'POST'])
@login_required
def post(post_id):
    post = Post.query.filter_by(id=post_id).first()

    author_state = State.query.filter_by(is_author=True, post_id=post.id).first()
    author = User.query.filter_by(id=author_state.user_id).first() # a user

    commenter_state = State.query.filter_by(is_author=False, post_id=post.id)
    commenter = [] # a list of users
    for state in commenter_state:
        commenter += User.query.filter_by(id=state.user_id).all()

    if current_user.id == author_state.user_id: is_authen=True
    else: is_authen=False

    form = CommentForm()
    if form.validate_on_submit():
        state = State(is_author=False, user_id=current_user.id,
                      post_id=post.id, comment=form.content.data)
        db.session.add(state)
        db.session.commit()
        return redirect(url_for("post", post_id=post.id))

    return render_template('post.html', form=form, author=author, post=post,
                           commenter=commenter[::-1],
                           commenter_state=commenter_state[::-1],
                           is_authen=is_authen)


@app.route('/post/update', methods=['GET', 'POST'])
@owner_only
@login_required
def update_post():
    post_id = request.args.get('post_id')
    post = Post.query.filter_by(id=post_id).first()
    form = PostForm(
        title=post.title,
        content=post.content,
        image_cover=post.image_cover
    )
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        post.image_cover = form.image_cover.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('post', post_id=post.id))
    return render_template('update_post.html', post=post, form=form)


@app.route('/post/<int:post_id>/delete', methods=['GET', 'POST'])
@login_required
def delete_post(post_id):
    post = Post.query.filter_by(id=post_id).first()
    states = State.query.filter_by(post_id=post.id)
    for state in states:
        db.session.delete(state)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('home'))

def send_reset_mail(user):
    token = user.get_reset_token()
    msg = Message(sender='noreply@demo.com', recipients=[user.email])
    msg.subject = 'Password Reset Request'
    msg.body = f'''To reset your password, visit the following link: 
{ url_for('reset_password', token=token, _external=True) } 

If you did not make this request then simply ignore this email and no change will be made.
'''
    mail.connect()
    mail.send(msg)


@app.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    form = RequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_mail(user)
        flash('An email has been sent with instructions to reset your password', 'success')
        return redirect(url_for('login'))
    return render_template('reset_request.html', form=form)


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    user = User.verify_reset_token(token)
    if user is None:
        flash('This is an invalid or expired token!', 'danger')
        return redirect(url_for('reset_request'))
    form = ResetForm()
    if form.validate_on_submit():
        hash_password = bcrypt.generate_password_hash(form.password.data)
        user.password = hash_password
        db.session.commit()
        flash('Your password has been updated. You are now able to login', 'success')
        return redirect(url_for('login'))
    return render_template('reset_password.html', form=form)


