""" util.auth2: Authentication tools

    This module is based off of util.auth, except with the action
    paradigm removed.
"""

from flask import session

from app.models import Account
from app.util import course as course_util

# Session keys
SESSION_EMAIL = 'email'

def create_account(email: str, password: str, first_name: str,
                   last_name: str, fsuid: str, course_list: list = []):
    """
    Creates an account for a single user.

    :email: Required, the email address of the user.
    :password: Required, user's chosen password.
    :first_name: Required, user's first name.
    :last_name: Required, user's last name.
    :fsuid: Optional, user's FSUID.
    :course_list: Optional, courses being taken by user
    :return: Account object.
    """

    account = Account(
        email=email,
        first_name=first_name,
        last_name=last_name,
        fsuid=fsuid,
        is_admin=False
    )

    # Set user's extra credit courses
    course_util.set_courses(account, course_list)

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
