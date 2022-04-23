
from flask import Flask, render_template
import os

IMG_FOLDER = os.path.join('static', 'img')

## Initialize the app in main file
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = IMG_FOLDER

## Home web page
@app.route('/')
def home():
    full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'layeta.svg')
    return render_template("home.html", user_image = full_filename)

## Pagina About
@app.route('/about')
def about():
    full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'layeta.svg')
    return render_template("about.html", user_image = full_filename)

## Pagina Login
@app.route('/login')
def login():
    full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'layeta.svg')
    return render_template("login.html", user_image = full_filename)

## Initialize server
if __name__ == '__main__':
    app.run(debug=True)