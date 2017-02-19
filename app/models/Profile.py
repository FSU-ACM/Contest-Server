from app import db

class Profile(db.Document):
    fname = db.StringField(required=True)
    lname = db.StringField(required=True)
    fsuid = db.StringField(unique=True)
    dob = db.DateTimeField()
    gender = db.StringField()
    race = db.StringField()
    foodallergies = db.StringField()
    major = db.StringField()
    year = db.StringField()
    gradyear = db.IntField()
    gradterm = db.StringField()
    advProg = db.StringField()
    status = db.StringField()

    # Account relationship
    team = db.ReferenceField('Team')

    def __repr__(self):
        if self.fsuid is not None:
            return '<Profile %r>' % self.fsuid
        else:
            return super(Profile, self).__repr__()
