# views.team.leave

from flask import redirect, url_for, render_template, request, session, abort

from app import app, recaptcha, db
from app.models import Account, Team
from app.util.views.auth import *

@app.route('/account/team/leave', methods=['POST'])
def team_leave():
    """
    This route allows a user to leave their team.
    """

    error, success = None, None

    # Access account (n/a throws 404)
    action, account = get_account(session)

    # Green means go
    if not action:

        # Retrieve team
        team = account.team

        # Attempt to leave
        try:
            account.team = None
            account.save()

            team.members.remove(account)

            # Clear name if last member
            if len(team.members) is 0:
                team.members = []
                team.teamName = None
            team.save()

            success = "You have left the team."
        except Exception as e:
            print e
            abort(500)

        action = redirect(url_for('team', success=success, error=error))

    return action
