
from flask import Flask, render_template
import os

IMG_FOLDER = os.path.join('static', 'img')

## Initialize the app in main file
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = IMG_FOLDER

## Home web page
@app.route('/')
def main():
    filename_logo = os.path.join(app.config['UPLOAD_FOLDER'], 'layeta.svg')
    return render_template("home.html", user_image = filename_logo)

## Home web page
@app.route('/home')
def home():
    filename_logo = os.path.join(app.config['UPLOAD_FOLDER'], 'layeta.svg')
    return render_template("home.html", user_image = filename_logo)

## Pagina About
@app.route('/about')
def about():
    filename_logo = os.path.join(app.config['UPLOAD_FOLDER'], 'layeta.svg')
    return render_template("about.html", user_image = filename_logo)

## Pagina Pronosticos
@app.route('/pronostics')
def pronostics():
    filename_logo = os.path.join(app.config['UPLOAD_FOLDER'], 'layeta.svg')
    return render_template("pronostics.html", user_image = filename_logo)

## Pagina Resultados Detallados
@app.route('/details')
def results():
    filename_logo = os.path.join(app.config['UPLOAD_FOLDER'], 'layeta.svg')
    return render_template("details.html", user_image = filename_logo)

## Pagina Login
@app.route('/login')
def login():
    filename_logo = os.path.join(app.config['UPLOAD_FOLDER'], 'layeta.svg')
    return render_template("login.html", user_image = filename_logo)

## Initialize server
if __name__ == '__main__':
    app.run(debug=True)