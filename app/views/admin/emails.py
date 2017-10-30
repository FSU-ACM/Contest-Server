# views.admin.emails

from flask import jsonify

from app import app, basic_auth
from app.models import Account


@app.route('/admin/emails')
@basic_auth.required
def get_emails():
    """
    This view prints all emails on screen, delimited by \n.
    """

    emails = [account.email for account in Account.objects.all()]
    return jsonify(emails)
