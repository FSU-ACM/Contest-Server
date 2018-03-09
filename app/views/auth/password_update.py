# views.account.update_password

from flask import (abort, flash, redirect, request, render_template,
    url_for,)

from app import app, recaptcha
from app.forms import ChangePassword as UpdatePasswordForm
from app.util import session as session_util
from app.util.auth2 import get_account
from app.views.generic import AccountFormView

class UpdatePasswordView(AccountFormView):
    """Update a logged in user's password

    """

    def get_template_name(self):
        return 'form2/update_password.html'

    def get_form(self):
        return UpdatePasswordForm()

    def post(self):
        form = UpdatePasswordForm(request.form)

        if form.validate():

            old_pass = form.current_password.data
            new_pass = form.new_password.data
            account = session_util.get_account()

            if account.check_password(old_pass):
                account.set_password(new_pass)
                account.save()
                flash("New password saved", 'success')
            else:
                # flash("That's not your current password.", 'error')
                form.current_password.errors.append(
                    "That's not your current password."
                )

        return self.render_template(form=form)

# @app.route('/account/updatepassword', methods=['POST', 'GET'])
# def updatepassword():
#     error, success = None, None

#     # check if the user is logged in. If not, return to the login page
#     if 'email' not in session:
#         return redirect(url_for('login'))

#     if request.method == 'POST':
#         email = session['email']
#         currentpassword = request.form['currentpassword']
#         newpassword = request.form['newpassword']

#         # Check if the old password is corect
#         account = Account.objects(email=email).first()
#         if not account.check_password(currentpassword):
#             error = "That's not your current password."
#         elif newpassword == currentpassword:
#             error = "New password cannot be same as the current password"
#         else:
#             account.set_password(newpassword)
#             account.save()
#             success = "Password updated successfully"

#     return render_template('/form2/updatepassword.html', error=error, success=success)
