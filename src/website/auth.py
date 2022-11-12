from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User, Fixture
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
import os
import csv
from datetime import datetime

IMG_FOLDER = os.path.join('static', 'img')
filename_logo = os.path.join(IMG_FOLDER, 'layeta_inv.png')
auth = Blueprint('auth', __name__)
FIXTURE_PATH = 'website/static/info/seriea_fixture.csv'
USERS_PATH = 'website/static/info/users.csv'

def init_db():
    # Get users from database
    cursor = db.session.execute("SELECT id FROM User ORDER BY id ASC")
    users_db = cursor.fetchall()
    if users_db == []:
        # Initialize database Users
        with open(USERS_PATH) as users_csv:
            users_file = csv.reader(users_csv, delimiter=',')
            for row in users_file:
                new_user = User(email=row[0],
                                first_name=row[1],
                                password=row[2])
                db.session.add(new_user)
            try: db.session.commit()
            except: db.session.rollback()
    # Get fixtures from database
    cursor = db.session.execute("SELECT gameid FROM Fixture ORDER BY gameid ASC")
    fix_db = cursor.fetchall()
    if fix_db == []:
        # Init DB Fixture
        with open(FIXTURE_PATH) as fixture_csv:
            file = csv.reader(fixture_csv, delimiter=',')
            for fixrow in file:
                fixture = Fixture(gameid=int(fixrow[0]),
                                  stage=fixrow[1],
                                  team1=fixrow[2],
                                  team2=fixrow[3],
                                  date=datetime.strptime(fixrow[4], '%y/%m/%d %H:%M:%S'))
                db.session.add(fixture)
            try: db.session.commit()
            except: db.session.rollback()
    return True

# Login page
@auth.route('/login', methods=['GET', 'POST'])
def login():

    if not hasattr(login, "var_init_db"):
        login.var_init_db = False

    if not login.var_init_db:
        init_db()
        login.var_init_db = True

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                login_user(user, remember=True)
                return redirect(url_for('views.pronostics'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html",
                           user=current_user,
                           logo_image=filename_logo)

# Logout page
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))