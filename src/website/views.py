from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import User, Prode, Fixture, Results, Linkgames
from . import db
from .table_calc import *
import os
from werkzeug.security import generate_password_hash
import datetime

IMG_FOLDER = os.path.join('static', 'img')
filename_logo = os.path.join(IMG_FOLDER, 'layeta_inv.png')
views = Blueprint('views', __name__)
link1 = 'https://www.livescores.com/football/italy/serie-a/?tz=-3&date=20221112'
link2 = 'https://www.livescores.com/football/italy/serie-a/?tz=-3&date=20221113'

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

def get_results_from_db():
    # Get results from database
    cursor = db.session.execute("SELECT * FROM Results ORDER BY id ASC")
    wc_results = cursor.fetchall()
        
    game_results = []
    game = []
    for r in wc_results:
        # Get teams from fixture
        cursor = db.session.execute("SELECT team1, team2, stage FROM Fixture WHERE gameid = :gameid", {"gameid": r[0]})
        teams = cursor.fetchall()
        game = [r[0], teams[0][2], teams[0][0], r[1], r[2], teams[0][1], r[3]]
        game_results.append(game)
    
    return game_results

def order_links_with_db(links):        
    ordered_links = []
    # Read fixture from database
    cursor = db.session.execute("SELECT gameid, team1, team2 FROM Fixture ORDER BY gameid ASC")
    f = cursor.fetchall()
    for l in f:
        link = []
        team1 = l[1].replace(" ", "-").lower()
        team2 = l[2].replace(" ", "-").lower()
        if int(l[0]) <= 48:
            for link in links:
                if team1 in link and team2 in link:
                    ordered_links.append(link)
    # Append last 16 links
    ordered_links += links[48:]
                
    return ordered_links

def general_update_routine(link1,link2):    
    links1 = get_games_links(link1)
    links2 = get_games_links(link2)
    ordered_links = (links1 + links2)
    
    # Set Links in database
    i = 0
    for l in ordered_links:
        i += 1
        # Check if link is already in database
        cursor = db.session.execute("SELECT * FROM Linkgames WHERE id = :id", {"id": i})
        link_check = cursor.fetchall()
        if link_check == []:
            new_link = Linkgames(id=i, link=l)
            db.session.add(new_link)
        else:
            db.session.execute("Update Linkgames SET link = :link WHERE id = :id", {"link": l, "id": i})
                       
    games = get_all_games_from_links(ordered_links)
    for g in games:
        print(g)
    # Update Results in database
    for g in games:
        if "?" in g[1][1]:
            state = "NS"
        else:
            state = g[1][4]
            
        # Check if game is in database
        cursor = db.session.execute("SELECT * FROM Results WHERE id = :id", {"id": g[0]})
        game_check = cursor.fetchall()
        
        if game_check == []: 
            new_result = Results(id=g[0], team1goals=g[1][1], team2goals=g[1][2], state=state)
            db.session.add(new_result)
        else:
            db.session.execute("UPDATE Results SET team1goals = :team1goals, team2goals = :team2goals, state = :state WHERE id = :id", {"team1goals": g[1][1], "team2goals": g[1][2], "id": g[0], "state": state})
            db.session.execute("UPDATE Fixture SET team1 = :team1, team2 = :team2 WHERE gameid = :gameid", {"team1": g[1][0], "team2": g[1][3], "gameid": g[0]})
    
    db.session.commit()
            
    return True

def update_result_from_date():
    # Get Fixture from database
    cursor = db.session.execute("SELECT gameid, date FROM Fixture ORDER BY gameid ASC")
    fixture_dates = cursor.fetchall()
    # Remove last 7 characters from date
    fixture_dates = [[x[0], x[1][:-7]] for x in fixture_dates]
    fixture_dates = [[x[0],  datetime.datetime.strptime(x[1], '%Y-%m-%d %H:%M:%S')] for x in fixture_dates]
    
    date = datetime.datetime.utcnow()-datetime.timedelta(hours=3)
    #date = datetime.datetime(2022, 11, 25, 13, 1, 0)
    #date = datetime.datetime(2022, 12, 2, 16, 45, 0)
    date_limit = date - datetime.timedelta(hours=3)
    # Keep only dates from last 3 hours
    fixture_dates = [x for x in fixture_dates if x[1] < date]
    fixture_dates = [x for x in fixture_dates if x[1] > date_limit]
    
    for games in fixture_dates:
        # Get link from database
        cursor = db.session.execute("SELECT link FROM Linkgames WHERE id = :id", {"id": int(games[0])})
        l = cursor.fetchall()
        results = get_all_games_from_links(l[0])
        for r in results:
            r[0] = games[0]
        # Update Results in database        
            if "?" in r[1][1]:
                state = "NS"
            else:
                state = r[1][4] 
            db.session.execute("UPDATE Results SET team1goals = :team1goals, team2goals = :team2goals, state = :state WHERE id = :id", {"team1goals": r[1][1], "team2goals": r[1][2], "id": r[0], "state": state})
            db.session.execute("UPDATE Fixture SET team1 = :team1, team2 = :team2 WHERE gameid = :gameid", {"team1": r[1][0], "team2": r[1][3], "gameid": r[0]})
    
    db.session.commit()
        
    return True

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
    
    # Get fixture from db
    fix = get_fixture_from_db() 
    
    return render_template("pronostics.html",
                           user=current_user,
                           fixture=fix,
                           logo_image=filename_logo,
                           username=current_user.first_name,
                           time=datetime.datetime.utcnow()-datetime.timedelta(hours=3))
                           #time=datetime.datetime(2022, 12, 2, 16, 1, 0)) ## Out of date test

# General Result webpage
@views.route('/results', methods=['GET', 'POST'])
@login_required
def results():
    
    # Get fixture from db
    fix = get_fixture_from_db()
    # Get all users from db
    users = get_users_from_db()
    # Get all prodes from db
    prod = get_prodes_from_db(users) 
    
    if request.method == 'POST':
        general_update_routine(link1,link2)
                
    update_result_from_date()    
    game_results = get_results_from_db()    
    #print(game_results)
    #game_results[0] = [1, 'Group A', 'Qatar', '1', '1', 'Ecuador', 'FT']
    #game_results[1] = [2, 'Group B', 'England', '3', '0', 'Iran', 'FT']
    #game_results[2] = [3, 'Group A', 'Senegal', '2', '2', 'Netherlands', 'FT']
    #game_results[3] = [4, 'Group B', 'USA', '2', '1', 'Wales', 'HT']
    #game_results[4] = [5, 'Group C', 'Argentina', '5', '0', 'Saudi Arabia', '60m']
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
                           time=datetime.datetime.utcnow()-datetime.timedelta(hours=3))
                           #time=datetime.datetime(2022, 12, 2, 16, 15, 0)) ## Passed games test

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
