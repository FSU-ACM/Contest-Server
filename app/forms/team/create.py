from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField
from wtforms.validators import DataRequired, Length

from app.models import Team


class CreateTeam(FlaskForm):
    """Create a new team.

    This form lets a registered user create a new team and then
    automatically join the created team.

    """

    team_name = StringField('Team Name', validators=[Length(min=3, max=35)])
    division = RadioField('Division', choices=Team.DIVISIONS, validators=[DataRequired()])
    submit = SubmitField('Create Team')
