# views.team.leave

from flask import redirect, url_for, render_template, request, session, abort

from app import app, recaptcha, db
from app.models import Account, Team
from app.util.auth import get_account
from app.util.team import leave_team

import logging


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
            success = leave_team(account, team)
        except Exception as e:
            logging.error(e)
            abort(500)

        action = redirect(url_for('team', success=success, error=error))

    return action
