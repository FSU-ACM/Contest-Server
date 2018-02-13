# util.error

class UnauthorizedUserError(Exception):

    """Custom unauthorization error.

    This error is specifically to be thrown by FormView.authorize if
    the user fails the subclass's criteria. Please see FormView for
    more details.

    """

    pass
