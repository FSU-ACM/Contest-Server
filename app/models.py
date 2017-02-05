from app import db
from sqlalchemy.types import TypeDecorator, Unicode

class CoerceUTF8(TypeDecorator):
    """Safely coerce Python bytestrings to Unicode
    before passing off to the database."""

    impl = Unicode

    def process_bind_param(self, value, dialect):
        if isinstance(value, str):
            value = value.decode('utf-8')
        return value



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


class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    team_name = db.Column(CoerceUTF8(120), unique=False)
    username = db.Column(db.String(120), unique=False)
    password = db.Column(db.String(120), unique=False)

    def __init__(self, team_name, username, password):
        self.team_name = team_name
        self.username = username
        self.password = password

    def __repr__(self):
        return '<Team %r>' % self.team_name

    def csv(self, include_students=False):

        part1 = "{0},{1},{2}".format(self.username, self.password,
            self.team_name.encode('utf-8'))

        if include_students:
            for student in self.students:
                part1+=(","+str(student.fsuid))

        return part1

class Preregistration(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120),unique=True)
    name = db.Column(db.String(120),unique=False)

    def __init__(self, email, name=None):
        self.email=email
        self.name=name

    def __repr__(self):
        return '<Prereg {0},{1}>'.format(self.name,self.email)
   

class SignIn(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fsuid = db.Column(db.String(64))

    def __init__(self, fsuid):
        self.fsuid = fsuid

    def __repr__(self):
        return '<sign_in %r>' % self.fsuid

