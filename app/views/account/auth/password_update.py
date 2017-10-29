# views.account.update_password

from flask import redirect, url_for, render_template, request, session

from app import app
from app.models import Account


@app.route('/account/updatepassword', methods=['POST', 'GET'])
def updatepassword():
    error, success = None, None

    # check if the user is logged in. If not, return to the login page
    if 'email' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        email = session['email']
        currentpassword = request.form['currentpassword']
        newpassword = request.form['newpassword']

        # Check if the old password is corect
        account = Account.objects(email=email).first()
        if not account.check_password(currentpassword):
            error = "That's not your current password."
        elif newpassword == currentpassword:
            error = "New password cannot be same as the current password"
        else:
            account.set_password(newpassword)
            account.save()
            success = "Password updated successfully"

    return render_template('/form/updatepassword.html', error=error, success=success)
