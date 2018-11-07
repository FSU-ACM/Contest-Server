from app import db


class Profile(db.Document):

    RACE = (
        ('', ''),
        ('American Indian or Native Alaskan',
            'American Indian or Native Alaskan'),
        ('Asian', 'Asian'),
        ('Black or African American',
            'Black or African American'),
        ('Hispanic', 'Hispanic'),
        ('Native Hawaiian or other Pacific Islander',
            'Native Hawaiian or other Pacific Islander'),
        ('White', 'White'),
    )

    GENDER = (
        ('', ''),
        ('Male', 'Male',),
        ('Female', 'Female',),
        ('Non-Binary', 'Non-Binary',),
    )

    GRAD_TERM = (
        ('', ''),
        ('Spring', 'Spring'),
        ('Summer', 'Summer'),
        ('Fall', 'Fall'),
    )

    STUDENT_STATUS = (
        ('', ''),
        ('Undergraduate', 'Undergraduate'),
        ('Graduate', 'Graduate'),
        ('High School', 'High School'),
        ('Non-degree Seeking', 'Non-degree Seeking'),
    )

    ADV_COURSE = (
        ('', ''),
        ('COP3014', 'COP3014'),
        ('COP3330', 'COP3330'),
        ('COP4530', 'COP4530'),
        ('COP4531', 'COP4531'),
    )

    # dob = db.DateTimeField(null=True)
    age = db.IntField()
    gender = db.StringField(choices=GENDER)
    # race = db.ListField(db.StringField(choices=RACE))
    race = db.StringField(choices=RACE)
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

    def __str__(self):
        return str(self.id)
