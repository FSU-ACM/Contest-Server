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
def page_error(e):
    return render_template('500.html'), 500


@app.route('/allteams')
def allteams():
    teams = Team.objects.filter(team_name__exists=True)
    teams = [t for t in teams if any(member.profile for member in t.members)]
    return render_template('allteams.html', teams=teams)


from . import account
from . import admin
from . import auth
from . import nav
from . import register
from . import team

class Route:
    def __init__(self, url, view):
        self.url, self.view = url, view

routes = [
    Route('/register', register.SoloRegisterView.as_view('register')),

    Route('/login', auth.LoginView.as_view('login')),
    Route('/logout', auth.LogoutView.as_view('logout')),
    Route('/reset_password', auth.ResetPasswordView.as_view('reset_password')),

    Route('/account/profile', account.ProfileView.as_view('profile')),
    Route('/account/team', team.TeamView.as_view('team')),
    Route('/account/team/create', team.CreateView.as_view('team_create')),
    Route('/account/team/add', team.AddView.as_view('team_add_member')),
    Route('/account/team/leave', team.LeaveView.as_view('team_leave'))
]

[app.add_url_rule(route.url, view_func=route.view) for route in routes]
