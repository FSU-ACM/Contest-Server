from app import SignIn

class SignIn(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fsuid = db.Column(db.String(64))

    def __init__(self, fsuid):
        self.fsuid = fsuid

    def __repr__(self):
        return '<sign_in %r>' % self.fsuid
