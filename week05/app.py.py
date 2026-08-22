from flask import Flask, render_template, flash, redirect, url_for
from forms import RegisterationForm, LoginForm
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

app = Flask(__name__, static_url_path='/assets')
app.config['SECRET_KEY'] = 'f71684f1cfe7a13de2c29dfd80c4b294'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)



class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    #應付貼文多對一的情形
    posts = db.relationship('Post', backref='Author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone.utc))
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}', '{self.content}')"

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

@app.route("/")
def home():
    name = "Amber"
    return render_template("index.html",name=name,posts=posts)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/login", methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'blog@blog.com' and form.password.data == 'password':
            flash('You have been logged in!','success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username or password.','danger')
    return render_template("login.html",form=form,title="login")

@app.route("/register", methods=['GET','POST'])
def register():
    form = RegisterationForm()
    if form.validate_on_submit():
        flash(f'Account created for { form.username.data }!', 'success')
        return redirect(url_for('home'))
    return render_template("register.html",form=form,title='register')

@app.route("/oldlogin")
def oldlogin():
    user = "User"
    title = "Login"
    return render_template("old_login.html",user=user,title=title,items="abcdefg")

@app.route("/second")
def second():
    name = "Amber"
    return render_template("second_index.html",name=name) 

if __name__ == "__main__":
    app.run(debug=True)