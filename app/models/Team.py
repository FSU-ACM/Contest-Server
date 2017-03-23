from app import db

class Team(db.Document):

    MAX_NAME_LENGTH = 30

    teamName = db.StringField()

    # For joining the team in the db
    teamID    = db.StringField(required=True, unique=True)
    teamPass  = db.StringField(required=True)

    # Password for domjudge
    domPass   = db.StringField(required=True)

    # List of participants on team
    members = db.ListField(db.ReferenceField('Profile'), null=True)

    # Block editing
    shadowban = db.BooleanField()



    def __repr__(self):
        if self.team_name is not None:
            return '<Team %r>' % self.teamName
        else:
            return super(Team, self).__repr__()

    # def csv(self, include_students=False):
    #
    #     part1 = "{0},{1},{2}".format(self.domuser, self.dompass,
    #         self.team_name.encode('utf-8'))
    #
    #     if include_students:
    #         for student in self.students:
    #             part1+=(","+str(student.fsuid))
    #
    #     return part1
