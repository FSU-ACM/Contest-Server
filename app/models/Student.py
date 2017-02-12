from app import db

class Student(db.Model):
    fsuid = db.Column(db.String(64), primary_key=True)
    first_name = db.Column(db.String(20), unique=False)
    last_name = db.Column(db.String(20), unique=False)
    email = db.Column(db.String(120), unique=True)

    # category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    # category = db.relationship('Category',
    #     backref=db.backref('posts', lazy='dynamic'))

    team_id = db.Column(db.Integer, db.ForeignKey('team.id'))
    team = db.relationship('Team',
        backref=db.backref('students', lazy='dynamic'))

    def __init__(self, fsuid, email=None, first=None, last=None):
        self.fsuid = fsuid
        self.first_name = first
        self.last_name = last
        self.email = email

    def __repr__(self):
        return '<Student %r>' % self.fsuid
