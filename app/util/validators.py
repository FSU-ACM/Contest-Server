from wtforms.validators import ValidationError
from app.models import Account

class UnusedEmail(object):
    """
    Validate that the email is not linked to an account already.
    """
    def __init__(self, message=None):
        if not message:
            message = u'This email is already linked to an account.'
        self.message = message

    def __call__(self, form, field):
        if Account.objects(email=field.data).first():
            raise ValidationError(self.message)


class RegisteredEmail(object):
    """
    Validate that this email is registered.
    """
    def __init__(self, message=None):
        if not message:
            message = u'This email is not registered.'
        self.message = message

    def __call__(self, form, field):
        if not Account.objects(email=field.data).first():
            raise ValidationError(self.message)
