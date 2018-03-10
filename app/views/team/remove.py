from flask import flash, redirect, request, url_for
from flask.views import View

from app import app
from app.util import team as team_util
from app.util import auth2 as auth_util
from app.util import session as session_util

from .team import TeamView

class RemoveTeamMemberView(TeamView):
    """Remove a member from the user's team.

    """

    def post(self):
        return redirect(url_for('team'))

    def get(self):
        uid = request.args.get('uid', None)
        account = session_util.get_account()

        if account.team and uid:
            rm_account = auth_util.get_account(uid)
            team_util.leave_team(rm_account, account.team)
            flash("Removed {} from your team".format(uid))

        return redirect(url_for('team'))
