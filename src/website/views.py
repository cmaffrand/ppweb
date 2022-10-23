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
    
    # Get fixture from db
    cursor = db.session.execute("SELECT * FROM Fixture ORDER BY gameid ASC")
    wc_fixture = cursor.fetchall()
    # Remove 7 last characters from date
    wc_fixture = [[x[0], x[1], x[2], x[3], x[4][:-7]] for x in wc_fixture]
    # Format date to datetime
    wc_fixture = [[x[0], x[1], x[2], x[3], datetime.datetime.strptime(x[4], '%Y-%m-%d %H:%M:%S')] for x in wc_fixture]
    
    return render_template("pronostics.html",
                           user=current_user,
                           fixture=wc_fixture,
                           logo_image=filename_logo,
                           username=current_user.first_name,
                           time=datetime.datetime.utcnow()-datetime.timedelta(hours=3))
                           #time=datetime.datetime(2022, 11, 25, 13, 1, 0)) ## Out of date test

# General Result webpage
@views.route('/results')
@login_required
def results():
    
    # Get fixture from db
    cursor = db.session.execute("SELECT * FROM Fixture ORDER BY gameid ASC")
    wc_fixture = cursor.fetchall()
    # Remove 7 last characters from date
    wc_fixture = [[x[0], x[1], x[2], x[3], x[4][:-7]] for x in wc_fixture]
    # Format date to datetime
    wc_fixture = [[x[0], x[1], x[2], x[3], datetime.datetime.strptime(x[4], '%Y-%m-%d %H:%M:%S')] for x in wc_fixture]
    # Get all prodes from db
    cursor = db.session.execute("SELECT user_id, date, team1goals, team2goals, gameid FROM Prode ORDER BY gameid DESC")
    wc_prodes = cursor.fetchall()    
    print(wc_prodes)
    # Remove 7 last characters from date
    wc_prodes = [[x[0], x[1][:-7], x[2], x[3], x[4]] for x in wc_prodes]
    # Format date to datetime
    wc_prodes = [[x[0], datetime.datetime.strptime(x[1], '%Y-%m-%d %H:%M:%S'), x[2], x[3], x[4]] for x in wc_prodes]
    # Get all users from db
    cursor = db.session.execute("SELECT * FROM User ORDER BY id ASC")
    wc_users = cursor.fetchall()
    # Replace User ID by User Name in Prode table
    wc_prodes = [[wc_users[x[0]-1][3], x[1], x[2], x[3], x[4]] for x in wc_prodes]
    # Make integer game id and goals
    wc_prodes = [[x[0], x[1], int(x[2]), int(x[3]), int(x[4])] for x in wc_prodes]
    # Get all game results
    #game_results = get_all_games(link,1)
    game_results = [[1, 'Group A', 'Qatar', '1', '1', 'Ecuador', '22/11/20 13:00:00'], [2, 'Group B', 'England', '3', '0', 'Iran', '22/11/21 10:00:00'], [3, 'Group A', 'Senegal', '2', '2', 'Netherlands', '22/11/21 13:00:00'], [4, 'Group B', 'USA', '2', '1', 'Wales', '22/11/21 16:00:00'], [5, 'Group C', 'Argentina', '5', '0', 'Saudi Arabia', '22/11/22 07:00:00']]
    # Get every user overall score from db
    cursor = db.session.execute("SELECT first_name, score FROM User ORDER BY score DESC")
    users_score = cursor.fetchall()
    # Add enumed users score to list
    users_score = [[i+1, users_score[i][0], users_score[i][1]] for i in range(len(users_score))]
    return render_template("results.html",
                           user=current_user,
                           fixture=wc_fixture,
                           prodes=wc_prodes,
                           users=wc_users,
                           logo_image=filename_logo,
                           username=current_user.first_name,
                           game_results=game_results,
                           users_score=users_score,
                           time=datetime.datetime.utcnow()-datetime.timedelta(hours=3))
                           #time=datetime.datetime(2022, 11, 25, 13, 1, 0)) ## Passed games test

# Fixture webpage
@views.route('/fixture')
@login_required
def fixture():
    # Get fixture from db
    cursor = db.session.execute("SELECT * FROM Fixture ORDER BY gameid ASC")
    wc_fixture = cursor.fetchall()
    return render_template("fixture.html",
                           user=current_user,
                           fixture=wc_fixture,
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
