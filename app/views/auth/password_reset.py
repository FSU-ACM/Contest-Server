# views.account.password_reset

from flask import redirect, url_for, request, flash

from app.forms import ResetPassword as ResetPasswordForm
from app.util import email as email_util
from app.util import password as pass_util
from app.util.auth2 import get_account
from app.views.generic import FormView


class ResetPasswordView(FormView):

    def authorize(self):
        return get_account() is None

    def redirect_unauthorized(self):
        return redirect(url_for('login'))

    def get_template_name(self):
        return 'form2/reset_password.html'

    def get_form(self):
        return ResetPasswordForm()

    def post(self):
        form = ResetPasswordForm(request.form)

        if form.validate():
            account = form.account
            new_pass = pass_util.reset_password(account)

            email_util.reset_password_email(account.email, new_pass)
            flash("Password email sent.", "success")
            return redirect(url_for('login'))

        return self.render_template(form)
