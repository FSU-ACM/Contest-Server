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
