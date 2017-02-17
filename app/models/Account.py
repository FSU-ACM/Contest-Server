from app import db

class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), unique=False, nullable=False)
    password = db.Column(db.Date, unique=False, nullable=False)

    # category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    # category = db.relationship('Category',
    #     backref=db.backref('posts', lazy='dynamic'))

    profile_id = db.Column(db.Integer, db.ForeignKey('profile.id'))
    profile = db.relationship('Profile',uselist=False,back_populates='Profile')

    def __init__(self,id,email,password):
        self.id = id
        self.email = fsuid
        self.name = name


    def __repr__(self):
        return '<Account %r>' % self.email
