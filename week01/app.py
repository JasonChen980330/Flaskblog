from flask import Flask
import random
app = Flask(__name__)

@app.route("/")
@app.route("/home")
def home():
    return "<h1>This is homepage</h1>"

@app.route("/about")
def about():
    return "<h1>This is about page</h1>" 
 
@app.route('/add/<int:a>/<int:b>')
def add(a, b):
    return f'{a} + {b} = {a+b}'
 
@app.route('/random/<int:min>/<int:max>')
def get_random(min, max):
    r = random.randint(min, max)
    return f'{r}'

if __name__=='__main__':
    app.run(debug=True)