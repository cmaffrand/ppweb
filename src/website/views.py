from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note
from . import db
import json
import os

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


@views.route('/pronostics')
@login_required
def pronostics():
    return render_template("pronostics.html",
                           user=current_user,
                           logo_image=filename_logo,
                           username=current_user.first_name)

# General Result and Pronostic webpage


@views.route('/results')
@login_required
def results():
    return render_template("results.html",
                           user=current_user,
                           logo_image=filename_logo,
                           username=current_user.first_name)
