# views.register.quick_register

from flask import redirect, url_for, render_template, request, session

from app import app, recaptcha
from app.models import Account, Team
from app.util.auth import verify_email
from app.util.team import *
from app.util.password import make_password
from app.util.email import quick_register_email
from app.util.auth import get_account

import bleach

@app.route('/quickregister', methods=['GET'])
def quick_register():

    error = request.args.get('error', None)
    success = request.args.get('success', None)

    # Disuade double registering
    action, account = get_account(session)
    action = None if not account else redirect(url_for('profile',
        message="You are already registered!"))

    if not action:
        action = render_template('/form/quick_register.html', error=error, success=success)

    return action

@app.route('/quickregister', methods=['POST'])
def quick_register_post():

    error, success = None, None

    form = request.form.to_dict()

    # Collect details
    name = request.form['teamname']
    emails = [
        bleach.clean(form.get('email1', None)),
        bleach.clean(form.get('email2', None)),
        bleach.clean(form.get('email3', None))
    ]
    emails = [e for e in emails if e is not None]
    emails = [e for e in emails if e != ""]
    accounts = []

    # Make sure this is done
    if not recaptcha.verify():
        error = "Please complete the ReCaptcha."

    # Verify all emails
    if not error:
        for email in emails:
            if not verify_email(email):
                console.log(email)
                error = "Please submit valid emails."
                break

    # Make sure these emails do not have accounts
    if not error:
        for email in emails:
            if Account.objects(email=email).first():
                error = "%s is already registered." % email

    # If no validation errors...
    if not error:

        # Create accounts
        for email in emails:
            account = Account(email=email)
            password = make_password()
            account.set_password(password)
            account.save()
            quick_register_email(account.email, password)
            accounts.append(account)

        # Put on team, send email
        first = True
        while len(accounts) > 0:
            account = accounts.pop(0)
            team = None
            if first:
                team = create_team(account, name)
                first = False
            else:
                error, x = join_team(account, team=team)
            if error:
                break

    action = None
    if error:
        action = redirect(url_for('quick_register', error=error))
    else:
        action = redirect(url_for('login', success="Check your email for your password!"))

    return action
