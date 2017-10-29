from app import db


class Course(db.Document):
    courseName = db.StringField()
    courseID = db.StringField()
    profEmail = db.EmailField()

    # Students in the course
    students = db.ListField(db.ReferenceField('Profile'), null=True)
