# views.team.leave

from flask import redirect, url_for, render_template, request, session, abort

from app import app, recaptcha, db
from app.models import Profile, Team
from app.util.views.auth import *

@app.route('/profile/team/leave', methods=['POST'])
def team_leave():
    """
    This route allows a user to leave their team.
    """

    error, success = None, None

    # Access profile (n/a throws 404)
    action, profile = verify_profile(session)

    # Green means go
    if not action:

        # Retrieve team
        team = profile.team

        # Attempt to leave
        try:
            profile.team = None
            profile.save()

            team.members.remove(profile)

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
