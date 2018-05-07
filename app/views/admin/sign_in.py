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
    """SignInView: For checking in contest attendees.

    This is *not* LoginView, where users can log in to the system
    in order to edit their information.

    SignInView is only accessible for accounts with the is_admin flag
    toggled. Everyone else gets redirected to the /login page.

    As of 5/2018, the profile is required to be complete before login.
    There is an outstanding issue to remove the profile from the site.
    You'll still need to be a member of a team to sign in though.

    Successfully signing in will toggle an email to be sent, see
    sign_in_email.
    """

    def authorize(self):
        account = session_util.get_account()
        return account.is_admin is True

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
