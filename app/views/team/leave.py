# views.team.leave

from flask import redirect, url_for

from app.util import session as session_util
from app.util.team import leave_team
from .team import TeamView


class LeaveTeamView(TeamView):
    """Leave a team.

    """

    def get(self):
        account = session_util.get_account()

        # Try leaving the team. If they're not on one, that's fine too.
        if account.team:
            leave_team(account, account.team)

        return redirect(url_for('team'))

    def post(self):
        return self.get()
