# views.admin.emails

from io import StringIO
import csv

from flask import make_response

from app import app, basic_auth
from app.models import Account


@app.route('/admin/users/csv')
@basic_auth.required
def user_csv():
    """
    Downloads a CSV containing user data elements:
        - Email
        - First Name
        - Last Name
        - FSUID
        - Team Name
        - Team ID
    """
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
