# util.views.auth

from flask import redirect, url_for
from app.models import Account, Profile
import re

# Email validator
EMAIL_REGEX = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")


# Auth tools
def verify_login(session):
    """
    Validates the user is logged in, otherwise redirects to
    the login page.
    """
    if 'email' not in session or 'profile_id' not in session:
        return redirect(url_for('login')), None, None
    else:
        return None, session['email'], session['profile_id']


def get_account(session):
    """
    Retrieves account via email in session, otherwise redirects
    to login page.
    """
    if 'email' not in session:
        return redirect(url_for('login')), None
    else:
        account = Account.objects.get_or_404(email=session['email'])
        return None, account


def verify_profile(session):
    """
    Validates the user has created a profile, otherwise redirects
    to the profile page.
    """
    if 'profile_id' not in session:
        return redirect(url_for('profile', error="You need a profile to complete this action.")), None
    else:
        profile = Profile.objects.get_or_404(id=session['profile_id'])
        return None, profile


def verify_email(email):
    """
    Validates an input string matches the email template.
    """
    return EMAIL_REGEX.match(email)
