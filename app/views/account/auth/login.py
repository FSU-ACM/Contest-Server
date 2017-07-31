# views.account.auth.login

from flask import redirect, url_for, render_template, request, session, abort

from app import app, recaptcha
from app.models import Account
from app.views._util.auth import *

import bleach

@app.route('/login',methods=['POST','GET'])
def login():

    # maybe enable after checking security
    # if 'email' in session and 'profile_id' in session:
    #     return redirect('/profile', code=302)

    # error = request.args.get('error', None)
    error = request.args.get('error', None)
    success = request.args.get('success', None)
    insertrecaptcha = False

    # Activate recaptcha if too many bad attempts
    if 'counter' in session and session['counter'] >= 3:
        insertrecaptcha = True


    # Getting information from form
    if request.method =='POST':
        email = bleach.clean(request.form['email'])
        password = bleach.clean(request.form['password'])

        # Check valid Email
        if not verify_email(email):
            error = "Please submit a valid email."
        # verify that the password is not empty
        elif not password:
            error = "Please enter a valid password."
        # If we needed recaptcha, make sure they have it
        elif insertrecaptcha and not recaptcha.verify():
            error = "Please complete the ReCaptcha."

        # Check accounts if we don't have an error yet
        if error is None:

            account = Account.objects(email=email).first()
            correctpwd = account.check_password(password) if account else False

            # SUCCESS
            if account and correctpwd:
                session['email']=email
                return redirect(url_for('profile'), code=302)
            # FAILURE : Incorrect Password
            elif account and not correctpwd:
                #If login fails 3rd time and beyond, make user enter recaptcha
                session['counter']=session.get('counter',0)+1
                if session['counter'] >= 3:
                    insertrecaptcha = True # Turn reCaptcha in login on
                    error = "You have made too many incorrect login attempts. Please verify that you are not a robot."
                else:
                    error = "Invalid password."
            # FAILURE : Email not (register)ed.
            else:
                error = "This email is not registered."

    return render_template('/form/login.html',error=error, success=success, insertrecaptcha=insertrecaptcha)
