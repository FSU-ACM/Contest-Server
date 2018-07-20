from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Optional

from app.util.fields import EmailField, FSUIDField
from app.util.validators import UnusedEmail


class SoloRegister(FlaskForm):
    """SoloRegister

    This form lets someone register an account without creating
    an associated team. This gets used for people creating accounts
    to join a friend's team after they already created their team.

    """

    email = EmailField('Email', validators=[
        Email(),
        UnusedEmail()
    ])

    password = PasswordField('Password', validators=[
        DataRequired()
    ])

    first_name = StringField('First Name', validators=[
        DataRequired()
    ])

    last_name = StringField('Last Name', validators=[
        DataRequired()
    ])

    fsuid = FSUIDField('FSUID', validators=[
        Optional(strip_whitespace=True)
    ])

    submit = SubmitField('Register')
