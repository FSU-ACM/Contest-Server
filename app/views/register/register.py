# views.register.register

from flask import redirect, url_for, render_template, request, session, abort

from app import app, recaptcha
from app.models import Account, Preregistration, Profile, Team
from app.util.auth import *
from app.util.request import get_email, get_password

import bleach


@app.route('/register', methods=['POST', 'GET'])
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

                # Let's see if they preregistered
                prereg = Preregistration.objects(email=email).first()
                account.prereg = prereg if prereg else None

                # DB transactions
                account.save()

                # Set cookie, redirect to profile page.
                session['email'] = email
                action = redirect(url_for('profile'), code=302)

            else:
                error = "This email is already linked to an another account."

        action = action if action is not None else \
            render_template('/form/register.html', error=error)

    return action
