# views.team.team

from flask import redirect, url_for, render_template, request, session, abort

from app import app, recaptcha, db
from app.models import Account, Team
from app.util.auth import *
from app.util.team import create_team

import bleach

@app.route('/account/team', methods=['GET'])
def team():
    """
    Here a user can either view their team details if
    on a team, otherwise have the options to create
    or join a team.
    """

    error = request.args.get('error', None)
    success = request.args.get('success', None)

    # Access account (throws 404)
    action, account = get_account(session)

    if not action:

        # Let's see if they have a team
        team = account.team

        action = render_template('/form/profile_team.html', team=team,
            account=account, error=error, success=success)

    return action


@app.route('/account/team', methods=['POST'])
def team_create():
    """
    This route is for creating a new team.
    """

    error, success = None, None

    # Access the account (n/a throws 404)
    action, account = get_account(session)

    # Make sure they're not already on a team
    action = None if (action is None and not account.team) else action or \
        redirect(url_for('team', error="You're already on a team!"))

    # Given account and no team:
    if not action:

        name = request.form['teamName']

        # Safety first!
        try:
            team = create_team(account, name)
        except:
            abort(500)

        action = redirect(url_for('team'))

    return action
