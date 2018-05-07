# util.team

from flask import flash

from app import app
from app.models import Team
from app.util.password import make_password


def create_team(account, name):
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
        team.members = [account]
    else:
        team.members.append(account)
    account.team = team

    # Set the team name
    rename_team(team, (name or team.teamID))
    team.save()
    account.save()

    return team


def set_division(team, division):
    """Set team's division

    This is called three times:
        1. When a team is created from a registed solo user
        2. When a team is quick registered
        3. When a team is updated/renamed

    1 and 2 are part of a creation process, but are called separately
    from the create_team method.

    """
    team.division = division
    validate_division(team)
    team.save()
    # TODO make this more...robust


def join_team(account, teamID=None, teamPass=None, team=None):

    # Look up the team if we didn't bring one
    if team is None:
        team = Team.objects(teamID=teamID, teamPass=teamPass).first()

    # We didn't bring a team nor did we find one
    if team is None:
        error = "Team with those credentials not found."

    # We have our team, let's try joining
    if team:
        if len(team.members) < 3:
            team.members.append(account)
            account.team = team
            validate_division(team)
            team.save()
            account.save()
            return True
        else:
            flash("Team already has 3 members", 'danger')
            return False

    flash("Error finding team", 'danger')
    return False


def leave_team(account, team):
    account.team = None
    account.save()

    team.members.remove(account)

    # Clear name if last member, change teampass
    if len(team.members) is 0:
        team.members = []
        team.team_name = None
        team.division = None
        team.teamPass = make_password()
    team.save()

    success = "You have left the team."

    return success


def rename_team(team, name):
    team.team_name = name
    team.team_name = team.team_name[:Team.MAX_NAME_LENGTH]
    team.save()

    success = "Team name updated."

    return success


def validate_division(team):
    """Validates that all team members qualify for the
    marked division.

    This is called three times:
        1. From set_division (see method comment)
        2. From join_team.
        3. From a profile update.

    Both times we make sure a team is not formed/updated against the rules.

    """

    division = int(team.division)

    if division is 2:
        app.logger.debug("????")
        for member in team.members:
            if member.profile:
                if member.profile.adv_course is 'COP4530' or member.profile.adv_course is 'COP4531':
                    team.division = 1
                    flash("Based a team member's furthest course, we've automatically promoted your team to Upper Division", 'info')
                    return
