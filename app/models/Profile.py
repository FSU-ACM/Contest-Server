from app import db


class Profile(db.Document):

    RACE = (
        ('AI', 'American Indian or Native Alaskan'),
        ('A', 'Asian'),
        ('B', 'Black or African American'),
        ('H', 'Hispanic'),
        ('PI', 'Native Hawaiian or other Pacific Islander'),
        ('W', 'White'),
    )

    GENDER = (
        ('M', 'Male',),
        ('F', 'Female',),
        ('N', 'Non-Binary',),
    )

    GRAD_TERM = (
        ('SP', 'Spring'),
        ('SM', 'Summer'),
        ('FA', 'Fall'),
    )

    STUDENT_STATUS = (
        ('U', 'Undergraduate'),
        ('G', 'Graduate'),
        ('HS', 'High School'),
        ('NS', 'Non-degree Seeking'),
    )

    ADV_COURSE = (
        ('COP3014', 'COP3014'),
        ('COP3330', 'COP3330'),
        ('COP4530', 'COP4530'),
        ('COP4531', 'COP4531'),
    )

    # dob = db.DateTimeField(null=True)
    age = db.IntField()
    gender = db.StringField(choices=GENDER)
    race = db.ListField(db.StringField(choices=RACE))
    food_allergies = db.StringField()
    major = db.StringField()
    grad_year = db.IntField()
    grad_term = db.StringField(choices=GRAD_TERM)
    adv_course = db.StringField(choices=ADV_COURSE)
    student_status = db.StringField(choices=STUDENT_STATUS)

    # Extra credit relationship
    # courses = db.ListField(db.ReferenceField('Course'), null=True)

    def __repr__(self):
        if self.fsuid is not None:
            return '<Profile %r>' % (self.firstname + ' ' + self.lastname)
        else:
            return super(Profile, self).__repr__()
