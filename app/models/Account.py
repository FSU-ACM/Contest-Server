from app import db
# from app.models import Profile, Preregistration

class Account(db.Document):
    email = db.StringField(primary_key=True, required=True, unique=True)
    password = db.StringField(required=True)
    profile = db.ReferenceField('Profile')
    prereg = db.ReferenceField('Preregistration')

    # profile_id = db.Column(db.Integer, db.ForeignKey('profile.id'))
    # profile = db.relationship('Profile', uselist=False, back_populates="account")

    # prereg_id = db.Column(db.Integer, db.ForeignKey('preregistration.id'))
    # prereg = db.relationship('Preregistration', uselist=False, back_populates="account")

    def __repr__(self):
        return '<Account %r>' % self.email
