from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email

from app.util.auth2 import get_account

class SignIn(FlaskForm):
    """SignIn Form

    Validates a user is okay to check in to the contest

    """

    email = StringField('Email', validators=[Email()])
    submit = SubmitField('Sign In')

    def validate(self):
        rv = FlaskForm.validate(self)
        if not rv:
            return False

        account = get_account(self.email.data)

        if account is None:
            self.email.errors.append('This email is not registered.')
            return False

        self.account = account
        return True
