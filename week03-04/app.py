from flask import Flask, render_template, flash, redirect, url_for
from forms import RegisterationForm, LoginForm
yee = Flask(__name__, static_url_path='/assets')

posts = [
    {
        'author': 'Corey Schafer',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'April 20, 2018'
    },
    {
        'author': 'Jane Doe',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'April 21, 2018'
    }
]

yee.config['SECRET_KEY'] = 'f71684f1cfe7a13de2c29dfd80c4b294'

@yee.route("/")
def home():
    name = "Amber"
    return render_template("index.html",name=name,posts=posts)

@yee.route("/about")
def about():
    return render_template("about.html")

@yee.route("/login", methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'blog@blog.com' and form.password.data == 'password':
            flash('You have been logged in!','success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username or password.','danger')
    return render_template("login.html",form=form,title="login")

@yee.route("/register", methods=['GET','POST'])
def register():
    form = RegisterationForm()
    if form.validate_on_submit():
        flash(f'Account created for { form.username.data }!', 'success')
        return redirect(url_for('home'))
    return render_template("register.html",form=form,title='register')

@yee.route("/oldlogin")
def oldlogin():
    user = "User"
    title = "Login"
    return render_template("old_login.html",user=user,title=title,items="abcdefg")

@yee.route("/second")
def second():
    name = "Amber"
    return render_template("second_index.html",name=name) 

if __name__ == "__main__":
    yee.run(debug=True)