# views.account.profile

from flask import flash, redirect, url_for, render_template, request, session, abort

from app import app
from app.forms import Profile as ProfileForm
from app.models import Account, Profile
from app.util import session as session_util, team as team_util
from app.views.generic import FormView, AccountFormView


import bleach, logging


class ProfileView(AccountFormView):
    """Collects extra data from user.

    Unauth'd users redirected to login.

    """

    def get_template_name(self):
        return 'form2/profile.html'

    def get_form(self):
        account = session_util.get_account()
        if account.profile:
            return ProfileForm(obj=account.profile)
        else:
            return ProfileForm()

    def post(self):
        form = ProfileForm(request.form)

        if form.validate():
            account = session_util.get_account()
            data = {field.name: field.data for field in form}
            del data['csrf_token']
            del data['submit']


            if not account.profile:
                account.profile = Profile(**data)
            else:
                account.profile.update(**data)

            account.profile.save()
            account.save()

            if account.team:
                team_util.validate_division(account.team)

            flash('Profile updated')

        return self.render_template(form=form)


