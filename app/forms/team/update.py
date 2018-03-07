from wtforms import SubmitField
from .create import CreateTeam

class UpdateTeam(CreateTeam):
    """Update a team's info.

    Basically the same as create team, but with different button
    text.

    """

    submit = SubmitField('Update Team')

