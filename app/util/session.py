from flask import session

from app import app
from app.models import Account
from app.util.errors import UnauthorizedUserError

SID = 'email'


def login(account: Account):
    """Save relevant account data in session

    :return: None
    """
    session[SID] = account.id
    # app.logger.debug("Added %s to session", account.id)


def logout():
    """Erase session data

    :return: None
    """
    del session[SID]


def is_auth():
    """Checks whether the user is authenticated.

    :returns: Whether user is logged in
    """
    # app.logger.debug("Is auth? %s", session.get(SID, None))
    return SID in session


def get_account():
    """Retrieve the account from the session.

    :return: Account object for logged in user.
    """
    try:
        # app.logger.debug("Get account? %s", session.get(SID, None))

        # Even though Account.email is the primary key, and
        # account.email == account.id == account.pk, performing
        # a get using id can't find it, so we uses pk for clarity.
        # We could also use email, but this seems better.
        return Account.objects.get_or_404(pk=session[SID])
    except:
        raise UnauthorizedUserError()
