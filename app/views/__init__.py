# app.views

from flask import render_template, jsonify
from app import app
from app.models import Team

@app.route('/')
def index():
    return render_template('index/index.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500

@app.route('/allteams')
def allteams():
    teams = Team.objects.filter(teamName__exists=True)
    teams = [t for t in teams if any(member.profile for member in t.members)]
    return render_template('allteams.html', teams=teams)

from . import account
from . import admin
from . import nav
from . import register
from . import team
# from . import views
