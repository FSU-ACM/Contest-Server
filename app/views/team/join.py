# views.team.join

from flask import redirect, url_for, render_template, request, session, abort

from app import app, recaptcha, db
from app.models import Profile, Team
from app.util.views.auth import *

@app.route('/profile/team/join', methods=['POST'])
def team_join():
    """
    This route allows a user to join a team.
    """

    error, success = None, None

    # Access profile (n/a throws 404)
    action, profile = verify_profile(session)

    # Perform join if profile exists
    if not action:

        # Team lookup
        teamID, teamPass = request.form['teamID'], request.form['teamPasscode']
        team = Team.objects(teamID=teamID,teamPass=teamPass).first()

        if team:

            # Max 3 members
            if not team.members:
                team.members = [profile] # See workaround notice above
                team.save()
                profile.team = team
                profile.save()
                success = "You joined the team!"
            elif len(team.members) < 3:
                team.members.append(profile)
                profile.team = team
                team.save()
                profile.save()
                success = "You joined the team!"
            else:
                error = "Team %s already has 3 members." % \
                    team.teamName or team.teamID
        else:
            error = "Team with those credentials not found."

        action = redirect(url_for('team', success=success, error=error))

    return action
