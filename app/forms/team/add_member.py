from flask_wtf import FlaskForm
from wtforms import SubmitField
from wtforms.validators import Email

from app.util.auth2 import get_account
from app.util.fields import EmailField

class AddMember(FlaskForm):
    """Add a member to a team.

    Submits an email address used to look up an account to be added
    to a team.

    """

    email = EmailField('Enter a registered email', validators=[Email()])
    submit = SubmitField('Add Member')

    def __init__(self, *args, **kwargs):
        FlaskForm.__init__(self, *args, **kwargs)
        self.add_account = None

    def validate(self):
        if not FlaskForm.validate(self):
            return False

        account = get_account(self.email.data)
        if not account:
            self.email.errors.append('This email is not registered.')
            return False

        if account.team:
            self.email.errors.append('Account is already on a team.')
            return False

        self.account = account
        return True
