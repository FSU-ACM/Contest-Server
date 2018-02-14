# views.register.register

from flask import (abort, flash, redirect, render_template, request, session,
    url_for,)

from app import app, recaptcha
from app.models import Account, Profile, Team
from app.util.auth import get_account, verify_email
from app.util.request import get_email, get_password
from app.util import auth2
from app.forms import SoloRegister

import bleach, logging

from app.views.generic import FormView

class SoloRegisterView(FormView):

    def authorize(self):
        session.account = auth2.get_account()
        logging.warn(session.account)
        return session.account is None

    def redirect_unauthorized(self):
        flash("You are already registered!", 'message')
        return redirect(url_for('profile'))

    def get_template_name(self):
        return 'form2/solo_register.html'

    def get_form(self):
        return SoloRegister()

    def post(self):
        form = SoloRegister(request.form)

        if form.validate():

            email, password = form.email.data, form.password.data

            account = Account(email=email)
            account.set_password(password)

            # DB transactions
            account.save()

            # Set cookie, redirect to profile page.
            session['email'] = email
            return redirect(url_for('profile'), code=302)

        return self.render_template(form=form)


# @app.route('/register', methods=['POST', 'GET'])
def register():
    error = request.args.get('error', None)
    success = request.args.get('success', None)

    # Disuade from registering twice
    action, account = get_account(session)
    action = None if not account else redirect(url_for('profile', message="You are already registered!"))

    if not action:

        if request.method == 'POST':

            # Validate login; deny or redirect to profile
            email = get_email()
            password = get_password()

            # Validate email
            if not verify_email(email):
                error = "Please submit a valid email."

            # Validate password
            elif not password:
                error = "Please enter a valid password."

            elif not recaptcha.verify():
                error = "Please complete the ReCaptcha."

            # SUCCESS STATE
            elif not Account.objects(email=email).first():
                # Create an account for our user
                account = Account(email=email)
                account.set_password(password)

                # DB transactions
                account.save()

                # Set cookie, redirect to profile page.
                session['email'] = email
                action = redirect(url_for('profile'), code=302)

            else:
                error = "This email is already linked to an another account."

        action = action if action is not None else \
            render_template('/form/register.html', success=success, error=error)

    return action
