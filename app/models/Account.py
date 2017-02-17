from app import db

class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), unique=False, nullable=False)
    password = db.Column(db.Date, unique=False, nullable=False)

    # category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    # category = db.relationship('Category',
    #     backref=db.backref('posts', lazy='dynamic'))

    # profile_id = db.Column(db.Integer, db.ForeignKey('profile.id'))
    profile = db.relationship('Profile', uselist=False, back_populates="account")

    # prereg_id = db.Column(db.Integer, db.ForeignKey('preregistration.id'))
    prereg = db.relationship('Preregistration', uselist=False, back_populates="account")

    def __init__(self,email,password):
        self.email = email
        self.password = password

    def __repr__(self):
        return '<Account %r>' % self.email
