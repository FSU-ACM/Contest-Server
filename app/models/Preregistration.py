from app import db

class Preregistration(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120),unique=True)
    name = db.Column(db.String(120),unique=False)

    # Account relationship
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'))
    account = db.relationship("Account", back_populates="prereg")


    def __init__(self, email, name=None):
        self.email=email
        self.name=name

    def __repr__(self):
        return '<Prereg {0},{1}>'.format(self.name,self.email)
