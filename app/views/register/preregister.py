# views.register.preregister

from flask import redirect, url_for, render_template, request, session, abort

from app import app, recaptcha
from app.models import Preregistration
from app.util.auth import *

import bleach


@app.route('/preregister', methods=['POST', 'GET'])
def preregister():
    error = None
    success = None

    # Getting information from formi
    if request.method == 'POST':
        name = bleach.clean(request.form['name'])
        email = bleach.clean(request.form['email'])

        # Verify recaptcha
        if not recaptcha.verify():
            error = "Please complete the ReCaptcha."

        # Check valid Email
        elif not verify_email(email):
            error = "Please submit a valid email."

        # Check unique email
        elif not Preregistration.objects(email=email).first():
            # Creating entry and inserting it into the database
            prereg = Preregistration(email=email, name=name)
            prereg.save()
            success = """Congratulations, {}, you are now preregistered for the contest! We'll contact you at your email ({}) when full registration opens.""".format(
                name, email)

        else:
            error = "This email is already registered."

    return render_template('/form/prereg.html', error=error, success=success)
