from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note, User, Prode, Fixture
from . import db
import json
import os
from werkzeug.security import generate_password_hash
import datetime

IMG_FOLDER = os.path.join('static', 'img')
filename_logo = os.path.join(IMG_FOLDER, 'layeta_inv.png')
views = Blueprint('views', __name__)

# Home webpage


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash('Note is too short!', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')

    return render_template("home.html",
                           user=current_user,
                           logo_image=filename_logo,
                           username=current_user.first_name)

# Delete note


@views.route('/delete-note', methods=['POST'])
@login_required
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})

# User Pronostic webpage


@views.route('/pronostics', methods=['GET', 'POST'])
@login_required
def pronostics():
    
    if request.method == 'POST':
        team1goals = request.form.get('team1goals')
        team2goals = request.form.get('team2goals')
        gameid = request.form.get('gameid')

        new_prode = Prode(team1goals=team1goals, team2goals=team2goals, gameid=gameid, user_id=current_user.id)
        db.session.add(new_prode)
        db.session.commit()
        flash('Pronostic Added!', category='success')
        
    print(datetime.datetime.utcnow()-datetime.timedelta(hours=3))
            
    return render_template("pronostics.html",
                           user=current_user,
                           logo_image=filename_logo,
                           username=current_user.first_name,
                           time=datetime.datetime.utcnow()-datetime.timedelta(hours=3))
                           #time=datetime.datetime(2022, 11, 25, 10, 1, 0)) ## Out of date test 
    
    ## Out of date test time=datetime(2022, 11, 25, 11, 0, 0)))

# General Result and Pronostic webpage


@views.route('/results')
@login_required
def results():
    return render_template("results.html",
                           user=current_user,
                           logo_image=filename_logo,
                           username=current_user.first_name)
    
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