from flask import Flask, render_template
yee = Flask(__name__, static_url_path='/assets')

@yee.route("/")
def home():
    name = "Amber"
    return render_template("index.html",name=name)

@yee.route("/login")
def login():
    user = "User"
    title = "Login"
    return render_template("login.html",user=user,title=title,items="abcdefg")

if __name__ == "__main__":
    yee.run(debug=True)
