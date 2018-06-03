""" util.auth2: Authentication tools

    This module is based off of util.auth, except with the action
    paradigm removed.
"""

from flask import session

from app.models import Account

# Session keys
SESSION_EMAIL = 'email'

def create_account(email: str, password: str, first_name: str,
                   last_name: str, fsuid: str):
    """
    Creates an account for a single user.

    :email: Required, the email address of the user.
    :password: Required, user's chosen password.
    :first_name: Required, user's first name.
    :last_name: Required, user's last name.
    :fsuid: Optional, user's FSUID.
    :return: Account object.
    """

    account = Account(
        email=email,
        first_name=first_name,
        last_name=last_name,
        fsuid=fsuid
    )

    account.set_password(password)
    account.save()

    return account

def get_account(email: str=None):
    """
    Retrieves account via email (defaults to using session), otherwise
    redirects to login page.

    :email: Optional email string, if not provided will use session['email']
    :return: Account if email is present in session, None otherwise.
    """

    try:
        email = email or session['email']
        return Account.objects.get_or_404(email=email)
    except:
        return None
