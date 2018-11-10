# app.views

from flask import render_template
from flask.views import View

from app import app
from app.models import Team

class IndexView(View):
    """Main index view

    """

    def dispatch_request(self):
        return render_template('index/index.html')

class TeamListView(View):
    """View listing all registered teams

    """

    def dispatch_request(self):
        teams = Team.objects.filter(team_name__exists=True, members__exists=True, division__exists=True)
        num_members = sum([len(team.members) for team in teams])
        return render_template('form2/allteams.html', teams=teams,
                                num_members=num_members)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('common/404.html'), 404


@app.errorhandler(500)
def page_error(e):
    return render_template('common/500.html'), 500


from . import account
from . import admin
from . import auth
from . import register
from . import team

class Route:
    def __init__(self, url, view):
        self.url, self.view = url, view

routes = [
    Route('/', IndexView.as_view('index')),
    Route('/teams', TeamListView.as_view('teams')),

    Route('/register', register.SoloRegisterView.as_view('register')),
    Route('/quickregister', register.QuickRegisterView.as_view('quick_register')),

    Route('/login', auth.LoginView.as_view('login')),
    Route('/logout', auth.LogoutView.as_view('logout')),
    Route('/reset_password', auth.ResetPasswordView.as_view('reset_password')),
    Route('/account/updatepassword', auth.UpdatePasswordView.as_view('update_password')),

    Route('/account', account.EditAccountView.as_view('account')),
    Route('/account/team', team.TeamView.as_view('team')),
    Route('/account/team/update', team.UpdateView.as_view('team_update')),
    Route('/account/team/create', team.CreateView.as_view('team_create')),
    Route('/account/team/add', team.AddView.as_view('team_add_member')),
    Route('/account/team/leave', team.LeaveView.as_view('team_leave')),
    Route('/account/team/remove', team.RemoveView.as_view('team_remove')),

    Route('/admin/signin', admin.SignInView.as_view('sign_in')),
]

[app.add_url_rule(route.url, view_func=route.view) for route in routes]
