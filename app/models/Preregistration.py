from app import db


class Preregistration(db.Document):
    email = db.StringField(unique=True, required=True)
    name = db.StringField(unique=False, null=True)

    def __repr__(self):
        return '<Preregistration %r>' % self.email
