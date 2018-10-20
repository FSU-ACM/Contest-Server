from werkzeug.security import generate_password_hash, check_password_hash

from app import db


class Account(db.Document):
    # Sign-in
    email = db.EmailField(required=True, primary_key=True)
    password = db.StringField(required=True)

    # Relationships
    team = db.ReferenceField('Team')
    profile = db.ReferenceField('Profile')

    # Core Info (Extra Credit)
    first_name = db.StringField(required=True)
    last_name = db.StringField(required=True)
    fsuid = db.StringField()
    signin = db.DateTimeField(null=True)

    # Admin status
    is_admin = db.BooleanField(null=True)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return '<Account %r>' % self.email

    def __str__(self):
        return self.first_name + " " + self.last_name

    def clean(self):
        """
        Make sure self.email is always lowercase. This function is
        automatically called on self.save()
        """
        self.email = self.email.lower()
