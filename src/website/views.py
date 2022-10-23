from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import User, Prode, Fixture
from . import db
from .table_calc import *
import os
from werkzeug.security import generate_password_hash
import datetime

IMG_FOLDER = os.path.join('static', 'img')
filename_logo = os.path.join(IMG_FOLDER, 'layeta_inv.png')
views = Blueprint('views', __name__)
link = "https://www.livescores.com/football/world-cup/"

# Home webpage
@views.route('/')
@login_required
def home():
    return pronostics()

# User Pronostic webpage
@views.route('/pronostics', methods=['GET', 'POST'])
@login_required
def pronostics():

    if request.method == 'POST':
        team1goals = request.form.get('team1goals')
        team2goals = request.form.get('team2goals')
        gameid = request.form.get('gameid')
        date = datetime.datetime.utcnow()-datetime.timedelta(hours=3)

        new_prode = Prode(team1goals=team1goals, team2goals=team2goals,
                          gameid=gameid, date=date, user_id=current_user.id)
        db.session.add(new_prode)
        db.session.commit()
        #flash('Pronostic Added!', category='success')

    return render_template("pronostics.html",
                           user=current_user,
                           logo_image=filename_logo,
                           username=current_user.first_name,
                           time=datetime.datetime.utcnow()-datetime.timedelta(hours=3))
                           #time=datetime.datetime(2022, 11, 25, 13, 1, 0)) ## Out of date test

# General Result webpage
@views.route('/results')
@login_required
def results():
    
    # Get all game results
    game_results = get_all_games(link,1)
    # For every user, get the prode score
    #db.session.query(User).update({User.score: 0})
    return render_template("results.html",
                           user=current_user,
                           logo_image=filename_logo,
                           username=current_user.first_name,
                           game_results=game_results)

# Fixture webpage
@views.route('/fixture')
@login_required
def fixture():
    return render_template("fixture.html",
                           user=current_user,
                           logo_image=filename_logo,
                           username=current_user.first_name)

# General Rules webpage
@views.route('/rules')
@login_required
def rules():
    return render_template("rules.html",
                           user=current_user,
                           logo_image=filename_logo,
                           username=current_user.first_name)
