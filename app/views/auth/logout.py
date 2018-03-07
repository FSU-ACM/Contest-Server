# views.account.auth.logout

from flask import redirect, url_for, session
from flask.views import View
from app import app
from app.util import session as session_util

class LogoutView(View):

    def dispatch_request(self):
        if session_util.is_auth():
            session_util.logout()

        return redirect(url_for('index'))

