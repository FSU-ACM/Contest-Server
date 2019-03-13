# util.team

from flask import flash

from app import app
from app.models import Team, Course
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

    This is called five times:
        1. When a team is created from a registed solo user
        2. When a team is quick registered
        3. When a team is updated/renamed
        4. When a user joins the team
        5. When a user edits their course list

    1 and 2 are part of a creation process, but are called separately
    from the create_team method.

    This will move the team into upper division if any upper level courses
    are found.

    """

    division = int(division)

    team.division = division

    # If setting to lower division, check courses of members
    if division == 2:    
        upper_courses = Course.objects(division=1)

        for t in team.members:
            if any((c in t.courses for c in upper_courses)):
                # Found an upper division course, can't be in lower
                team.division = 1

                flash("Team moved to upper division: a member is taking an upper division course!", 'danger')
                break
    
    team.save()


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

            # Update team's division
            if team.division == 2:
                set_division(team, team.division)

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

