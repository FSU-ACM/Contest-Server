from app import db

class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fsuid = db.Column(db.String(64), unique=True)
    name = db.Column(db.String(128), unique=False, nullable=False)
    dob = db.Column(db.Date, unique=False, nullable=False)
    gender = db.Column(db.String(64), unique=True)
    race = db.Column(db.String(64), unique=True)
    major = db.Column(db.String(64), unique=True)
    year = db.Column(db.String(64), unique=True)
    mostProg = db.Column(db.String(64), unique=True)

    # category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    # category = db.relationship('Category',
    #     backref=db.backref('posts', lazy='dynamic'))

    account_id = db.Column(db.Integer, db.ForeignKey('Account.id'))
    account = db.relationship('Account',back_populates='Account')

    def __init__(self, fsuid, name,email=None, gender=None):
        self.fsuid = fsuid
        self.name = name
        self.dob = dob
        self.gender = gender
        self.race = race
        self.major = major
        self.year = year
        self.mostProg = mostProg

    def __repr__(self):
        return '<Student %r>' % self.fsuid
