from app import db
from werkzeug.security import generate_password_hash, check_password_hash

class Account(db.Document):
    email = db.EmailField(required=True)
    password = db.StringField(required=True)
    profile = db.ReferenceField('Profile')
    prereg = db.ReferenceField('Preregistration')

    signin = db.DateTimeField(null=True)

    # Teams relationship
    team = db.ReferenceField('Team')


    # Handles password-things
    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


    def __repr__(self):
        return '<Account %r>' % self.email
