# views.account.auth.login

from flask import (redirect, request, url_for, )

from app.forms import Login as LoginForm
from app.util import session as session_util
from app.views.generic import FormView


class LoginView(FormView):
    """View to authenicate user.

    Checks username/password, adds account to session. Redirects already
    auth'd users to profile.

    """

    def authorize(self):
        return not session_util.is_auth()

    def redirect_unauthorized(self):
        return redirect(url_for('profile'))

    def get_template_name(self):
        return 'form2/login.html'

    def get_form(self):
        return LoginForm()

    def post(self):
        form = LoginForm(request.form)

        if form.validate():
            session_util.login(form.account)
            return redirect(url_for('profile'))

        return self.render_template(form=form)


    # TODO reintroduce recaptcha

    # # Activate recaptcha if too many bad attempts
    # if 'counter' in session and session['counter'] >= 3:
    #     insertrecaptcha = True

    # # If we needed recaptcha, make sure they have it
    #     elif insertrecaptcha and not recaptcha.verify():
    #         error = "Please complete the ReCaptcha."

    # # If login fails 3rd time and beyond, make user enter recaptcha
    #     session['counter'] = session.get('counter', 0) + 1
    #     if session['counter'] >= 3:
    #         insertrecaptcha = True  # Turn reCaptcha in login on
    #         error = "You have made too many incorrect login attempts. Please verify that you are not a robot."
    #     else:
    #         error = "Invalid password."

