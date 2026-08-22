import secrets, os
from PIL import Image
from flask import render_template, flash, redirect, url_for, request, abort
from flaskblog import app, db, bcrypt
from flaskblog.forms import RegisterationForm, LoginForm, UpdateAccountForm, PostForm
from flaskblog.models import User,Post
from flask_login import login_user, logout_user, current_user, login_required


@app.route("/")
def home():
    name = "Amber"
    posts = Post.query.all()
    return render_template("index.html",name=name,posts=posts)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/login", methods=['GET','POST'])
def login():
    #prevent user who has been logged in will be able to click
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        #old
        # if form.email.data == 'blog@blog.com' and form.password.data == 'password':
        #new: check email and password in db
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            # flash('You have been logged in!','success')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username or password.','danger')
    return render_template("login.html",form=form,title="login")

@app.route("/register", methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegisterationForm()
    if form.validate_on_submit():
        #week seven
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('UTF-8')
        user = User(username=form.username.data,email=form.email.data,password=hashed_password)
        db.session.add(user)
        db.session.commit()

        flash(f'Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))

        # old
        # flash(f'Account created for { form.username.data }!', 'success')
        # return redirect(url_for('home'))
    return render_template("register.html",form=form,title='register')

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

def save_pics(form_pics):
    random_hex = secrets.token_hex(8)
    #not to care about the picture's filename
    _, f_ext = os.path.splitext(form_pics.filename)
    pics_fn = random_hex + f_ext
    #connect multiple paths
    pics_path = os.path.join(app.root_path, 'static/profile_pics', pics_fn)

    output_size = (125, 125)
    i = Image.open(form_pics)
    i.thumbnail(output_size)
    i.save(pics_path)

    return pics_fn

@app.route("/account", methods=['GET','POST'])
@login_required
def account():
    form = UpdateAccountForm()
    image_file = url_for('static',filename=f"profile_pics/{current_user.image_file}")
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_pics(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template('account.html', title='Account', image_file=image_file, form=form)

@app.route("/post/new", methods=['GET','POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        # put post to db
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('create_post.html', title='New Post', form=form)

@app.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)

@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been Updated!', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post', form=form)

@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('home'))


@app.route("/oldlogin")
def oldlogin():
    user = "User"
    title = "Login"
    return render_template("old_login.html",user=user,title=title,items="abcdefg")

@app.route("/second")
def second():
    name = "Amber"
    return render_template("second_index.html",name=name)