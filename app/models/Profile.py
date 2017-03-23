from app import db

class Profile(db.Document):
    firstname = db.StringField(required=True)
    lastname = db.StringField(required=True)
    fsuid = db.StringField()
    dob = db.DateTimeField(null=True)
    gender = db.StringField()
    race = db.ListField(db.StringField())
    foodallergies = db.StringField()
    major = db.StringField()
    year = db.StringField()
    gradyear = db.IntField()
    gradterm = db.StringField()
    advProg = db.StringField()
    status = db.StringField()

    # Block editing
    shadowban = db.BooleanField()

    # Account relationship
    team = db.ReferenceField('Team')

    def __repr__(self):
        if self.fsuid is not None:
            return '<Profile %r>' % self.fsuid
        else:
            return super(Profile, self).__repr__()
