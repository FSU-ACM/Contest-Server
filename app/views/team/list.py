from flask import render_template
from flask.views import View

from app.models import Team

class TeamListView(View):
    """ View listing all registered teams """

    def dispatch_request(self):
        teams = Team.objects.filter(team_name__exists=True, members__exists=True, division__exists=True)
        num_members = sum([len(team.members) for team in teams])
        return render_template('form2/allteams.html', teams=teams,
                                num_members=num_members)
