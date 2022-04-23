
from flask import Flask, render_template

## Initialize the app in main file
app = Flask(__name__)

## Home web page
@app.route('/')
def home():
    return render_template('home.html')

## Pagina About
@app.route('/about')
def about():
    return render_template('about.html')

## Pagina About
@app.route('/login')
def login():
    return render_template('login.html')

## Initialize server
if __name__ == '__main__':
    app.run(debug=True)