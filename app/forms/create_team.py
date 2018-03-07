from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

class CreateTeam(FlaskForm):
    """CreateTeam

    This form lets a registered user create a new team and then
    automatically join the created team.

    """

    team_name = StringField('Team Name', validators=[
        DataRequired()
    ])

    submit = SubmitField('Create Team')

class RenameTeam(CreateTeam):
    """RenameTeam

    Same as CreateTeam, just has different button text.

    """

    submit = SubmitField('Rename Team')
