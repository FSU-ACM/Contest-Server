# views.admin.emails

import csv
from flask import make_response, redirect, url_for
from flask.views import View
from io import StringIO

from app.models import Account
from app.util import session as session_util


class UserCsvView(View):
    """Download a CSV with all user information (not passwords).

    Only accessible for is_admin accounts.

    Downloads a CSV containing user data elements:
    - Email
    - First Name
    - Last Name
    - FSUID
    - Team Name
    - Team ID
    """

    def dispatch_request(self):
        account = session_util.get_account()
        if not account.is_admin():
            return redirect(url_for('login'))
        else:

            users = [(
                account.id,
                account.first_name,
                account.last_name,
                account.fsuid,
                ((account.team and account.team.team_name) or ''),
                ((account.team and account.team.teamID) or ''),
                (account.signin is not None)
            ) for account in Account.objects.all()]

            # Add CSV header
            users.insert(0, (
                'Email',
                'First Name',
                'Last Name',
                'FSUID',
                'Team Name',
                'Team ID',
                'Checked In'
            ))

            si = StringIO()
            cw = csv.writer(si)
            cw.writerows(users)

            res = make_response(si.getvalue())
            res.headers['Content-Disposition'] = 'attachment; filename=mycsv.csv'
            res.mimetype = 'text/csv'
            return res
