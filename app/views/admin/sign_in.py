# views.admin.sign_in

from flask import flash, redirect, url_for, render_template, request, session

from app import app, basic_auth
from app.forms import SignIn as SignInForm
from app.models import Account, Profile, Team
from app.util import session as session_util
from app.util.email import sign_in_email
from app.util.auth import verify_email
from app.util.request import get_email
from app.views.generic import FormView

import datetime, re

class SignInView(FormView):
    """

    """

    def authorize(self):
        # Only Andrew
        # TODO fix this
        account = session_util.get_account()
        return account.email == "andrewsosa001@gmail.com"

    def redirect_unauthorized(self):
        return redirect(url_for('login'))

    def get_template_name(self):
        return 'admin/signin.html'

    def get_form(self):
        return SignInForm()

    def post(self):
        form = SignInForm(request.form)

        if form.validate():
            account = form.account

            if not account.profile:
                flash("You need to complete your profile first.", 'danger')
            elif not account.team:
                flash("You're not on a team!", 'danger')
            else:
                try:
                    sign_in_email(account.email, account.team.teamID,
                                  account.team.domPass)
                    account.signin = datetime.datetime.now
                    account.save()
                    flash("Welcome, %s!" % (account.email), 'success')
                except:
                    flash("There's been an issue sending your email. Go find Andrew!", 'danger')

            return redirect(url_for('sign_in'))

        return self.render_template(form=form)
