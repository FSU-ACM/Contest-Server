# views.team.join

from flask import redirect, url_for, render_template, request, session, abort

from app import app, recaptcha, db
from app.models import Account, Team
from app.util.views.auth import *

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

        # Team lookup
        teamID, teamPass = request.form['teamID'], request.form['teamPasscode']
        team = Team.objects(teamID=teamID,teamPass=teamPass).first()

        if team:

            # Max 3 members
            if not team.members:
                team.members = [account] # See workaround notice above
                team.save()
                account.team = team
                account.save()
                success = "You joined the team!"
            elif len(team.members) < 3:
                team.members.append(account)
                account.team = team
                team.save()
                account.save()
                success = "You joined the team!"
            else:
                error = "Team %s already has 3 members." % \
                    team.teamName or team.teamID
        else:
            error = "Team with those credentials not found."

        action = redirect(url_for('team', success=success, error=error))

    return action
