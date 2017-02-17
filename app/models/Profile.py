from app import db

class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    f_name = db.Column(db.String(128), unique=False, nullable=False)
    l_name = db.Column(db.String(128), unique=False, nullable=False)
    fsuid = db.Column(db.String(64), unique=True, nullable=True)
    dob = db.Column(db.Date, unique=False, nullable=False)
    gender = db.Column(db.String(64), unique=False)
    race = db.Column(db.String(64), unique=False)
    foodallergies = db.Column(db.String(512), unique=False)
    major = db.Column(db.String(64), unique=False)
    year = db.Column(db.String(64), unique=False)
    gradyear = db.Column(db.Integer, unique=False)
    gradterm = db.Column(db.String(64), unique=False)
    advProg = db.Column(db.String(64), unique=False)
    status = db.Column(db.String(64), unique=False)

    # Account relationship
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'))
    account = db.relationship("Account", back_populates="profile")

    team_id = db.Column(db.Integer,db.ForeignKey('team.id'))
    team = db.relationship("Team", back_populates="members")

    def __init__(self,f_name,l_name,account_id,team_id,dob,\
                 fsuid=None,gender=None,race=None,foodallergies=None,\
                 major=None,year=None,gradyear=None,gradterm=None,\
                 advProg=None,status=None):
        self.f_name = f_name
        self.l_name = l_name
        self.fsuid = fsuid
        self.dob = dob
        self.gender = gender
        self.race = race
        self.foodallergies = foodallergies
        self.major = major
        self.year = year
        self.gradyear = gradyear
        self.gradterm = gradterm
        self.advProg = advProg
        self.status = status
        self.account_id = account_id
        self.team_id = team_id

    def __repr__(self):
        return '<Student %r>' % self.fsuid
