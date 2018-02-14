""" util.auth2: Authentication tools

    This module is based off of util.auth, except with the action
    paradigm removed.
"""

from flask import session
from app.models import Account, Profile
from app.util.errors import UnauthorizedUserError
import re

# Email validator
EMAIL_REGEX = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")

# Session keys
SESSION_EMAIL = 'email'

def get_account():
    """
    Retrieves account via email in session, otherwise redirects
    to login page.

    :return: Account if email is present in session, None otherwise.
    """

    try:
        return Account.objects.get_or_404(email=session['email'])
    except:
        return None
