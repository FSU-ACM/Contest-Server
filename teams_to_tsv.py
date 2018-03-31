##############
# team_to_tsv script
#  Creates two tsv files for importing into domjudge
#  Team info gets stored inside teams.tsv in the following format
#       <team_id(int)> <external_id> <category_id> <team_name>
#  Account info gets stored inside acccounts.tsv in the following format
#       team <team-name> <user-name> <password> <teamid>
#
#   Import teams.tsv first, then accounts.tsv
#

# NOTE 1 : Domjudge doesn't insert teams with ID < 1

from app.models.Team import *

with open("teams.tsv", "w+") as teams_tsv, \
     open("accounts.tsv", "w+") as accounts_tsv:
    # Headers requiered by domjudge
    teams_tsv.write("teams\t1\n")
    accounts_tsv.write("accounts\t1\n")
    walkin_counter = 1
    for team in Team.objects.all():
        # Only make 100 walk-in accounts
        if walkin_counter > 101:
            break;
        # Accounts that are not in use are assigned to walk-ins
        if team.team_name is None:
            team.team_name = "".join(("Walk-in-", str(walkin_counter)))
            walkin_counter += 1
        # Empty team names are assign a dummy value
        if team.team_name.isspace():
            team.team_name = "UnnamedTeam"
        # Avoiding team number 0, refer to NOTE 1 in the header
        if team.teamID == "acm-0":
            continue

        teams_tsv.write(u"\t".join(
          [team.teamID.strip("acm-"),  # To only get ID number
           team.teamID,  # Set to external ID for exporting
           "2",  # Category ID of Participants Category - See footnote
           team.team_name.strip('\t'), # So tabs in team_name don't interfere
           '\n']))

        accounts_tsv.write(u"\t".join(
          ["team",
           team.team_name.strip('\t'), # So tabs in team_name don't interfere
           '{0}-{1}'.format('team', team.teamID.split('-')[1].zfill(3)),
           team.domPass,
           # team.teamID.strip("acm-"),  # To only get ID number
           '\n']))

#
#   FOOTNOTE: Team Category
#
#   This value determines the team_category. Domjudge's defaults are:
#       1 -> System
#       2 -> Self-Registered
#       3 -> Jury
#
#   Since System and Jury are meant for admin, we assign teams to being
#   "self-registered" because you can't self-register for our contests
#   anyway, and this is easier than making you create a new category first.
#
