# views.team.team

from flask import redirect, url_for, render_template, request, session, abort

from app import app, recaptcha, db
from app.models import Profile, Team
from app.util.views.auth import *

import bleach

@app.route('/profile/team', methods=['GET'])
def team():
    """
    Here a user can either view their team details if
    on a team, otherwise have the options to create
    or join a team.
    """

    error = request.args.get('error', None)
    success = request.args.get('success', None)

    # Access profile (throws 404)
    action, profile = verify_profile(session)

    if not action:

        # Let's see if they have a team
        team = profile.team

        action = render_template('/form/profile_team.html', team=team,
            profile=profile, error=error, success=success)

    return action


@app.route('/profile/team', methods=['POST'])
def team_create():
    """
    This route is for creating a new team.
    """

    error, success = None, None

    # Access the profile (n/a throws 404)
    action, profile = verify_profile(session)

    # Make sure they're not already on a team
    action = None if (action is None and not profile.team) else action or \
        redirect(url_for('team', error="You're already on a team!"))

    # Given profile and no team:
    if not action:

        """
        ATTENTION:
        The following code is a workaround for a bug in MongoEngine.
        When removing the last element from a ListField and saving
        the document, it removes the field from the document.
        Therefore, we first look for teams without the field before
        finding ones with it missing.
        """


        # Let's assign them a team
        team = Team.objects.filter(members__exists=False).first()

        if team is None:
            team = Team.objects.filter(members__size=0).first()

        # More workaround code
        if team.members is None:
            team.members = [profile]
        else:
            team.members.append(profile)
        profile.team = team

        # Set the team name
        team.teamName = request.form['teamName'] or team.teamID
        team.teamName = team.teamName[:Team.MAX_NAME_LENGTH]

        # Safety first!
        try:
            team.save()
            profile.save()
        except:
            abort(500)

        action = redirect(url_for('team'))

    return action
