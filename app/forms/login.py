from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField
from wtforms.validators import DataRequired, Email

from app.util.auth2 import get_account
from app.util.fields import EmailField


class Login(FlaskForm):
    """Login Form

    This form authenticates a user via email and password.

    We extend the self.validate function per this example snippet:
    http://flask.pocoo.org/snippets/64/

    """

    email = EmailField('Email', validators=[Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


    def __init__(self, *args, **kwargs):
        FlaskForm.__init__(self, *args, **kwargs)
        self.account = None

    def validate(self):
        rv = FlaskForm.validate(self)
        if not rv:
            return False

        account = get_account(self.email.data)

        if account is None:
            self.email.errors.append('This email is not registered.')
            return False

        if not account.check_password(self.password.data):
            self.password.errors.append('Incorrect password.')
            return False

        self.account = account
        return True
