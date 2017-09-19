# views.team.rename

from flask import redirect, url_for, render_template, request, session, abort

from app import app
from app.models import Team, Account
from app.util.views.auth import get_account

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
        try:
            team = account.team

            team.teamName = request.form['teamName'] or "Unnamed Team"
            team.teamName = team.teamName[:Team.MAX_NAME_LENGTH]
            team.save()
            sucess = "Team name updated."
        except:
            abort(500)

        action = redirect(url_for('team', success=sucess, error=error))

    return action
