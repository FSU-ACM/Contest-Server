# views.account.password_reset

from flask import redirect, url_for, request

from app import app
from app.models import Account
from app.util import email as email_util
from app.util import password as pass_util
from app.util.views import auth as auth_util


@app.route('/resetpassword', methods=['POST'])
def reset_password():

    error, success = None, None
    error_msg = "No such email on file."

    email = request.form['email']

    error = None if auth_util.verify_email(email) else error_msg

    if not error:

        account = Account.objects(email=email).first()

        if account:
            pwd = pass_util.reset_password(account)
            email_util.reset_password_email(email, pwd)
            success = "Password email sent."
        else:
            error = error_msg

    return redirect(url_for('login', success=success, error=error))
