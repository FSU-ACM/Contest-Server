from . import db

class Team(db.Document):
    MAX_NAME_LENGTH = 30

    DIVISIONS = (("1", "Upper Division"), ("2", "Lower Division"))

    team_name = db.StringField()

    # For joining the team in the db
    teamID = db.StringField(required=True, unique=True)
    teamPass = db.StringField(required=True)

    # Password for domjudge
    domPass = db.StringField(required=True)

    # Division field
    division = db.IntField(required=False)

    # List of participants on team
    members = db.ListField(db.ReferenceField("Account"), null=True)

    # Block editing
    shadowban = db.BooleanField()

    def __repr__(self):
        if self.team_name is not None:
            return "<Team %r>" % self.team_name
        else:
            return super(Team, self).__repr__()

    def __str__(self):
        if self.team_name:
            return self.team_name
        else:
            return ""
