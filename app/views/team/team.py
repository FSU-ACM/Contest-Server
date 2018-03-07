# views.team.team

from flask import redirect, url_for, render_template, request, session, abort, flash

from app import app, recaptcha, db
from app.forms import (
        CreateTeam as CreateTeamForm,
        UpdateTeam as UpdateTeamForm,
        AddTeamMember as AddMemberForm,
    )
from app.models import Account, Team
from app.util import session as session_util
from app.util.auth import *
from app.util.team import create_team
from app.views.generic import AccountFormView

class TeamView(AccountFormView):
    """View for Team management.

    This view displays forms for creating, updating, leaving, and adding
    members to a team. However, we don't accept POSTs for any of thoses
    here, thoses are in different subclasssed views.

    """

    def authorize(self):
        return session_util.is_auth()

    def redirect_unauthorized(self):
        return redirect(url_for('login'))

    def get_template_name(self):
        return 'form2/team.html'

    def get_form(self):
        return CreateTeamForm()

    def post(self):
        return redirect(url_for('team'))

    def render_template(self, **kwargs):
        """
        We need to render a different form based on whether the user
        is on a team or not.

        If account.team is None, we should let them create a new team
        using CreateTeamForm. Otherwise, we show all the options available
        to existing teams: Editing team details, adding/removing team
        members, or leaving the team.
        """
        account = session_util.get_account()

        if not account.team:
            create_form = kwargs.get('create_form', None) or self.get_form()
            return super().render_template(create_form=create_form)
        else:
            updateTeamForm = kwargs.get('update_form', None) \
                or UpdateTeamForm(team_name=account.team.team_name,
                                  division=account.team.division)

            addMemberForm = kwargs.get('add_form', None) \
                or AddMemberForm()

            return super().render_template(edit_form=updateTeamForm,
                                           add_form=addMemberForm)

