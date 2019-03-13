from app import app, db

from app.models import Account

class Course(db.Document):
    name = db.StringField(required=True)
    professor_name = db.StringField(null=False)
    professor_email = db.EmailField(null=False)
    division = db.IntField(required=True)

    @property
    def num_students(self):
        return Account.objects(courses__contains=self).count()

    def __repr__(self):
        if self.professor_name:
            return '<Course %r - %r>' % (self.name, self.professor_name)
        else:
            return '<Course %r>' % self.name

    def __str__(self):
        if self.professor_name:
            return self.name + " - " + self.professor_name
        else:
            return self.name

    def clean(self):
        """
        Make sure self.email is always lowercase. This function is
        automatically called on self.save()
        """
        if self.professor_email:
            self.professor_email = self.professor_email.lower()
