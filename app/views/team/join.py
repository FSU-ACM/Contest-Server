# views.team.join

from flask import redirect, url_for, render_template, request, session, abort

from app import app, recaptcha, db
from app.models import Account, Team
from app.util.auth import *
from app.util.team import join_team


@app.route('/account/team/join', methods=['POST'])
def team_join():
    """
    This route allows a user to join a team.
    """

    error, success = None, None

    # Access account (n/a throws 404)
    action, account = get_account(session)

    # Perform join if account exists
    if not action:
        teamID, teamPass = request.form['teamID'], request.form['teamPasscode']

        error, success = join_team(account, teamID=teamID, teamPass=teamPass)

        action = redirect(url_for('team', success=success, error=error))

    return action
