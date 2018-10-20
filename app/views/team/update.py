# views.team.update

from flask import redirect, url_for, request, flash

from app.forms import UpdateTeam as UpdateTeamForm
from app.util import session as session_util, team as team_util
from .team import TeamView

class UpdateTeamView(TeamView):
    """Update a team's information.

    """

    def get_form(self):
        return UpdateTeamForm()

    def post(self):
        update_form = UpdateTeamForm(request.form)

        if update_form.validate():
            try:
                account = session_util.get_account()
                team_util.set_division(
                    account.team,
                    update_form.division.data
                )
                team_util.rename_team(account.team, update_form.team_name.data)
                return redirect(url_for('team'))
            except:
                flash('Error updating team information.')

        return self.render_template(update_form=update_form)

    def get(self):
        return redirect(url_for('team'))

