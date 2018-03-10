from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Optional

from app.util.validators import UnusedEmail

class SoloRegister(FlaskForm):
    """SoloRegister

    This form lets someone register an account without creating
    an associated team. This gets used for people creating accounts
    to join a friend's team after they already created their team.

    """

    email = StringField('Email', validators=[
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

    fsuid = StringField('FSUID', validators=[
        Optional(strip_whitespace=True)
    ])

    submit = SubmitField('Register')
