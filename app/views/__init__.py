# app.views

from flask import render_template, jsonify
from app import app
from app.models import Team


@app.route('/')
def index():
    return render_template('index/index.html')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('common/404.html'), 404


@app.errorhandler(500)
def page_error(e):
    return render_template('common/500.html'), 500


@app.route('/teams')
def teams():
    teams = Team.objects.filter(team_name__exists=True)
    num_members = sum([len(team.members) for team in teams])
    return render_template('form2/allteams.html', teams=teams,
                            num_members=num_members)


from . import account
from . import admin
from . import auth
from . import register
from . import team

class Route:
    def __init__(self, url, view):
        self.url, self.view = url, view

routes = [
    Route('/register', register.SoloRegisterView.as_view('register')),
    Route('/quickregister', register.QuickRegisterView.as_view('quick_register')),

    Route('/login', auth.LoginView.as_view('login')),
    Route('/logout', auth.LogoutView.as_view('logout')),
    Route('/reset_password', auth.ResetPasswordView.as_view('reset_password')),
    Route('/account/updatepassword', auth.UpdatePasswordView.as_view('update_password')),

    Route('/account/profile', account.ProfileView.as_view('profile')),
    Route('/account/team', team.TeamView.as_view('team')),
    Route('/account/team/create', team.CreateView.as_view('team_create')),
    Route('/account/team/add', team.AddView.as_view('team_add_member')),
    Route('/account/team/leave', team.LeaveView.as_view('team_leave')),
    Route('/account/team/remove', team.RemoveView.as_view('team_remove')),
]

[app.add_url_rule(route.url, view_func=route.view) for route in routes]
