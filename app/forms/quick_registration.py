from flask_wtf import FlaskForm
from wtforms import ( StringField, PasswordField, BooleanField, SubmitField,
    RadioField )
from wtforms.validators import DataRequired, Length, Email, Optional

from app.models import Team
from app.util.validators import UnusedEmail

class QuickRegister(FlaskForm):
    """Quick Register

    """

    team_name = StringField('Team Name',
                            validators=[DataRequired(), Length(min=3, max=35)])
    division = RadioField('Division', choices=Team.DIVISIONS, validators=[DataRequired()])



    email1 = StringField('Email',
                         validators=[Email(), UnusedEmail()])
    email2 = StringField('Email',
                         validators=[],
                         filters=[lambda x: x or None])
    email3 = StringField('Email',
                         validators=[],
                         filters=[lambda x: x or None])

    first_name1 = StringField('First Name', validators=[DataRequired()])
    first_name2 = StringField('First Name', validators=[])
    first_name3 = StringField('First Name', validators=[])

    last_name1 = StringField('Last Name', validators=[DataRequired()])
    last_name2 = StringField('Last Name', validators=[])
    last_name3 = StringField('Last Name', validators=[])

    fsuid1 = StringField('FSUID', validators=[Optional(strip_whitespace=True)])
    fsuid2 = StringField('FSUID', validators=[Optional(strip_whitespace=True)])
    fsuid3 = StringField('FSUID', validators=[Optional(strip_whitespace=True)])

    submit = SubmitField('Register')

    def __init__(self, *args, **kwargs):
        FlaskForm.__init__(self, *args, **kwargs)
        self.account2, self.account3 = False, False

    def validate(self):
        if not FlaskForm.validate(self):
            return False

        email_validators = [Email(), UnusedEmail()]
        name_validators = [DataRequired()]
        fsuid_validators = [Optional(strip_whitespace=True)]

        all_fields = []

        if self.email2.data:
            fields2 = (
                self.email2.validate(self, extra_validators=[Email(), UnusedEmail()]),
                self.first_name2.validate(self, extra_validators=name_validators),
                self.last_name2.validate(self, extra_validators=name_validators),
                self.fsuid2.validate(self, extra_validators=fsuid_validators)
            )
            all_fields.extend(fields2)
            self.account2 = all(fields2)

        if self.email3.data:
            fields3 = (
                self.email3.validate(self, extra_validators=[Email(), UnusedEmail()]),
                self.first_name3.validate(self, extra_validators=name_validators),
                self.last_name3.validate(self, extra_validators=name_validators),
                self.fsuid3.validate(self, extra_validators=fsuid_validators)
            )
            all_fields.extend(fields3)
            self.account3 = all(fields3)

        return all(all_fields)
