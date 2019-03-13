from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectMultipleField
from wtforms.validators import DataRequired, Email, Optional

from app.util.fields import EmailField, FSUIDField, CoursesField
from app.util.validators import UnusedEmail

from bson import ObjectId


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

    courses = CoursesField('Extra Credit Courses', coerce=ObjectId, validators=[
        Optional()
    ])

    submit = SubmitField('Register')
