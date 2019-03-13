# views.register.register

from flask import (flash, redirect, request, url_for, )

from app.forms import SoloRegister
from app.util import auth2, session as session_util
from app.views.generic import FormView


class SoloRegisterView(FormView):
    """View for a user to register w/o team or teammates.

    """

    def authorize(self):
        return not session_util.is_auth()

    def redirect_unauthorized(self):
        flash("You are already registered!", 'message')
        return redirect(url_for('login'))

    def get_template_name(self):
        return 'form2/solo_register.html'

    def get_form(self):
        return SoloRegister()

    def post(self):
        form = SoloRegister(request.form)

        if form.validate():

            account = auth2.create_account(
                email=form.email.data,
                password=form.password.data,
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                fsuid=form.fsuid.data,
                course_list=form.courses.data
            )

            # Set cookie, redirect to login page (which will forward to team page).
            session_util.login(account)
            return redirect(url_for('login'), code=302)

        return self.render_template(form=form)
