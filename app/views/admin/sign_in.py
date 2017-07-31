# views.admin.sign_in

from flask import redirect, url_for, render_template, request, session

from app import app, basic_auth
from app.models import Account, Profile, Team
from app.email import sign_in_email
from app.views._util.auth import verify_email

import datetime, re

@app.route('/signin', methods=['POST', 'GET'])
@basic_auth.required
def sign_in():
    """
    This view is for contest volunteers to sign in attendees.
    """

    error = request.args.get('error', None)
    success = request.args.get('success', None)
    email = request.form.get('email', None)

    if request.method == 'POST':

        if email == None or email == '' or not verify_email(email):
            error = "Please enter a valid email."
        else:
            # Retrieve team data : email => account => profile => team
            account, team = None, None
            try:
                account = Account.objects(email=email).first()
                team = account.profile.team
            except:
                if account is None:
                    error = "No account found for email %s." % email
                elif account.profile is None:
                    error = "Please join a team before signing in."
                else:
                    error = "Mysterious error! Go find Andrew, he'll know what to do."

            # Check if on team
            if not team:
                error = "Please join a team before signing in."

            # Attempt send email
            if not error:
                try:
                    sign_in_email(email, team.teamID, team.domPass)
                    account.signin = datetime.datetime.now
                    account.save()
                    success = "Welcome, %s!" % (account.profile.firstname)
                except:
                    error = "There's been an issue sending your email. Go find Andrew!"

    return render_template('/admin/signin.html', error=error, success=success)
