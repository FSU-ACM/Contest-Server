# views.team.join

from flask import (flash, request, redirect, url_for, )

from app.forms import AddTeamMember as AddTeamMemberForm
from app.util import team as team_util, session as session_util
from .team import TeamView


class AddTeamMemberView(TeamView):
    """Add a member to a team

    """

    def get_form(self):
        return AddTeamMemberForm()

    def post(self):
        add_form = AddTeamMemberForm(request.form)

        if add_form.validate():
            add_account = add_form.account
            user_account = session_util.get_account()
            if team_util.join_team(add_account, team=user_account.team):
                flash("Added {} to your team".format(add_account.email))
            return redirect(url_for('team'))

        return self.render_template(add_form=add_form)

    def get(self):
        return redirect(url_for('team'))
