# views.team.rename

from flask import redirect, url_for, render_template, request, session, abort

from app import app
from app.models import Team, Account
from app.util.auth import get_account
from app.util.team import rename_team, set_division

import bleach

@app.route('/account/team/rename', methods=['POST'])
def team_update():
    """
    This route is for updating team names.
    """

    error, success = None, None

    # Access account (n/a throws 404)
    action, account = get_account(session)

    # Make sure they're on a team, but preserve an existing action
    action = None if (action is None and account.team) else action or \
        redirect(url_for('team', error="You need to be on a team to do that!"))

    # Given account and team, do:
    if not action:

        name = request.form['teamName'] or "Unnamed Team"
        division = request.form['division'] or None
        team = account.team

        try:
            set_division(team, division)
            success = rename_team(team, name)
        except:
            abort(500)

        action = redirect(url_for('team', success=success, error=error))

    return action
