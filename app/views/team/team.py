# views.team.team

from flask import redirect, url_for, render_template, request, session, abort, flash

from app import app, recaptcha, db
from app.forms import CreateTeam as CreateTeamForm, RenameTeam as RenameTeamForm
from app.models import Account, Team
from app.util import session as session_util
from app.util.auth import *
from app.util.team import create_team
from app.views.generic import FormView

class TeamView(FormView):
    """View for Team management.

    This view's POST handles creating a team. However, for leaving and
    renaming the team, we POST to different views. Those views don't have
    GET requests.

    """

    def authorize(self):
        return session_util.is_auth()

    def redirect_unauthorized(self):
        return redirect(url_for('login'))

    def get_template_name(self):
        return 'form2/team.html'

    def get_form(self):
        return CreateTeamForm()

    def post(self):
        form = CreateTeamForm(request.form)

        if form.validate():
            try:
                account = session_util.get_account()
                team = create_team(account, form.team_name.data)
                return redirect(url_for('team'))
            except:
                flash('Error creating team.')

        return self.render_template(form=form)

    def get(self):
        """
        We need to render a different form based on whether the user
        is on a team or not.

        If account.team is None, we should let them create a new team
        using CreateTeamForm. Otherwise, we show the rename or leave
        team options along with the team information.
        """
        account = session_util.get_account()
        form = self.get_form() if not account.team else RenameTeamForm(team_name=account.team.teamName)
        return self.render_template(form=form, account=account)


# @app.route('/account/team', methods=['GET'])
# def team():
#     """
#     Here a user can either view their team details if
#     on a team, otherwise have the options to create
#     or join a team.
#     """

#     error = request.args.get('error', None)
#     success = request.args.get('success', None)

#     # Access account (throws 404)
#     action, account = get_account(session)

#     if not action:
#         # Let's see if they have a team
#         team = account.team

#         action = render_template('/form/profile_team.html', team=team,
#             account=account, error=error, success=success)

#     return action


# @app.route('/account/team', methods=['POST'])
# def team_create():
#     """
#     This route is for creating a new team.
#     """

#     error, success = None, None

#     # Access the account (n/a throws 404)
#     action, account = get_account(session)

#     # Make sure they're not already on a team
#     action = None if (action is None and not account.team) else action or \
#         redirect(url_for('team', error="You're already on a team!"))

#     # Given account and no team:
#     if not action:

#         name = request.form['teamName']

#         # Safety first!
#         try:
#             team = create_team(account, name)
#         except:
#             abort(500)

#         action = redirect(url_for('team'))

#     return action
