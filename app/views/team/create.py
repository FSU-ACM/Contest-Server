# views.team.team

from flask import redirect, url_for, render_template, request, session, abort, flash

from app.forms import CreateTeam as CreateTeamForm
from app.util import session as session_util, team as team_util

from .team import TeamView

class CreateTeamView(TeamView):
    """Create a team.

    """

    def get_form(self):
        return CreateTeamForm()

    def post(self):
        create_form = CreateTeamForm(request.form)

        if create_form.validate():
            try:
                account = session_util.get_account()
                team = team_util.create_team(
                    account,
                    create_form.team_name.data
                )
                team_util.set_division(
                    team,
                    create_form.division.data
                )
                return redirect(url_for('team'))
            except:
                flash('Error creating team.')

        return self.render_template(create_form=create_form)

    def get(self):
        return redirect(url_for('team'))

