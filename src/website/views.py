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
LINK_FILTER = "/world-cup/"

def get_fixture_from_db():
    cursor = db.session.execute("SELECT * FROM Fixture ORDER BY gameid ASC")
    wc_fixture = cursor.fetchall()
    # Remove 7 last characters from date
    wc_fixture = [[x[0], x[1], x[2], x[3], x[4][:-7]] for x in wc_fixture]
    # Format date to datetime
    wc_fixture = [[x[0], x[1], x[2], x[3], datetime.datetime.strptime(x[4], '%Y-%m-%d %H:%M:%S')] for x in wc_fixture]
    return wc_fixture

def get_prodes_from_db(wc_users):    
    cursor = db.session.execute("SELECT user_id, date, team1goals, team2goals, gameid FROM Prode ORDER BY gameid DESC")
    wc_prodes = cursor.fetchall()    
    # Remove 7 last characters from date
    wc_prodes = [[x[0], x[1][:-7], x[2], x[3], x[4]] for x in wc_prodes]
    # Format date to datetime
    wc_prodes = [[x[0], datetime.datetime.strptime(x[1], '%Y-%m-%d %H:%M:%S'), x[2], x[3], x[4]] for x in wc_prodes]
    # Replace User ID by User Name in Prode table
    wc_prodes = [[wc_users[x[0]-1][3], x[1], x[2], x[3], x[4]] for x in wc_prodes]
    # Make integer game id and goals
    wc_prodes = [[x[0], x[1], int(x[2]), int(x[3]), int(x[4])] for x in wc_prodes]
    return wc_prodes

def get_users_from_db():    
    cursor = db.session.execute("SELECT * FROM User ORDER BY id ASC")
    wc_users = cursor.fetchall()
    return wc_users

def get_users_scores_from_db():
    cursor = db.session.execute("SELECT first_name, score FROM User ORDER BY score DESC")
    users_score = cursor.fetchall()
    # Add enumed users score to list
    users_score = [[i+1, users_score[i][0], users_score[i][1]] for i in range(len(users_score))]
    return users_score

def update_scores(results):
    # Calculate scores
    scores = calc_scores(results)
    # Update scores in database
    for i in range(len(scores)):
        db.session.execute("UPDATE User SET score = :score WHERE id = :id", {"score": scores[i], "id": i+1})
    db.session.commit()
    
def calc_scores(results):
    # Get usersid from database
    cursor = db.session.execute("SELECT id FROM User ORDER BY id ASC")
    usersid = cursor.fetchall()
    # Format result to team1goals, team2goals, gameid, date
    results = [[int(x[3]), int(x[4]), int(x[0]), x[6]] for x in results if x[6] != 'NS']
    # Initialize Score in zero for each results
    scores_by_user = [[0 for x in results] for y in usersid]
    for users in usersid:
        # Get prodes from database for userid ordered by date filter repeated gamesid
        cursor = db.session.execute("SELECT team1goals, team2goals, gameid FROM Prode WHERE user_id = :user_id ORDER BY date ASC", {"user_id": users[0]})
        user_prode = cursor.fetchall()
        # Format result to team1goals, team2goals, gameid as integer
        user_prode = [[int(x[0]), int(x[1]), int(x[2])] for x in user_prode]
        for prode in user_prode:
            if prode[2] <= len(results):
                if prode[2] <= 48:
                    vdp = 1
                elif prode[2] <= 56:
                    vdp = 2
                elif prode[2] <= 60:
                    vdp = 3
                elif prode[2] <= 63:
                    vdp = 4
                else:
                    vdp = 6
                    
                if prode[0] == results[prode[2]-1][0] and prode[1] == results[prode[2]-1][1]:
                    scores_by_user[users[0]-1][prode[2]-1] = 5*vdp                
                elif prode[0] - prode[1] == results[prode[2]-1][0] - results[prode[2]-1][1]:
                    scores_by_user[users[0]-1][prode[2]-1] = 4*vdp
                elif prode[0] > prode[1] and results[prode[2]-1][0] > results[prode[2]-1][1]:
                    scores_by_user[users[0]-1][prode[2]-1] = 3*vdp
                elif prode[0] < prode[1] and results[prode[2]-1][0] < results[prode[2]-1][1]:
                    scores_by_user[users[0]-1][prode[2]-1] = 3*vdp
                else:
                    scores_by_user[users[0]-1][prode[2]-1] = 0                                              
    # Sum scores for each game by every user
    scores = [sum(x) for x in scores_by_user]
    return scores

def re_arrange_game_id(results,fixture):
    for r in results:
        for f in fixture:
            if int(r[0]) <= 48 and int(f[0]) <= 48:
                if f[2] == r[2] and f[3] == r[5]:
                    r[0] = f[0]
    # Sort results by gameid
    results = sorted(results, key=lambda x: x[0])
    return results

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
    fix = get_fixture_from_db() 
    
    return render_template("pronostics.html",
                           user=current_user,
                           fixture=fix,
                           logo_image=filename_logo,
                           username=current_user.first_name,
                           time=datetime.datetime.utcnow()-datetime.timedelta(hours=3))
                           #time=datetime.datetime(2022, 11, 25, 13, 1, 0)) ## Out of date test

# General Result webpage
@views.route('/results')
@login_required
def results():
    
    # Get fixture from db
    fix = get_fixture_from_db()    
    # Get all users from db
    users = get_users_from_db()
    # Get all prodes from db
    prod = get_prodes_from_db(users)    
    # Get all game results
    game_results = get_all_games(link,True,LINK_FILTER,True)
    game_results = re_arrange_game_id(game_results,fix)
    ### Test hadcoded results
    game_results[0] = [1, 'Group A', 'Qatar', '1', '1', 'Ecuador', 'FT']
    game_results[1] = [2, 'Group B', 'England', '3', '0', 'Iran', 'FT']
    game_results[2] = [3, 'Group A', 'Senegal', '2', '2', 'Netherlands', 'FT']
    game_results[3] = [4, 'Group B', 'USA', '2', '1', 'Wales', 'HT']
    game_results[4] = [5, 'Group C', 'Argentina', '5', '0', 'Saudi Arabia', '60m']
    # Calculate and update Scores
    update_scores(game_results)
    
    # Get every user overall score from db
    users_score = get_users_scores_from_db()
    
    return render_template("results.html",
                           user=current_user,
                           fixture=fix,
                           prodes=prod,
                           users=users,
                           logo_image=filename_logo,
                           username=current_user.first_name,
                           game_results=game_results,
                           users_score=users_score,
                           #time=datetime.datetime.utcnow()-datetime.timedelta(hours=3))
                           time=datetime.datetime(2022, 11, 22, 8, 15, 0)) ## Passed games test

# Fixture webpage
@views.route('/fixture')
@login_required
def fixture():
    # Get fixture from db
    fix = get_fixture_from_db()
    
    return render_template("fixture.html",
                           user=current_user,
                           fixture=fix,
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
