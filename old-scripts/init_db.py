#!/usr/bin/env python

from app import db
from app.models import *
from xkcdpass import xkcd_password as xp

import csv


# create a wordlist from the default wordfile
# use words between 5 and 8 letters long
wordfile = xp.locate_wordfile()
mywords = xp.generate_wordlist(wordfile=wordfile, min_length=5, max_length=8)


db.create_all()

def test_data():
    andrew = Student(fsuid='as12x', first='Andrew',
        last='Sosa', email='sosa@cs.fsu.edu')
    preston = Student(fsuid='pwh11', first='Preston',
        last='Hamlin', email="hamlin@cs.fsu.edu")

    db.session.add(andrew)
    db.session.add(preston)
    db.session.commit()

    balrogs = Team(team_name='B.T. Balrogs', username='user',
        password='pass')

    preston.team = balrogs

    db.session.add(balrogs)
    db.session.commit()


val = 0

def get_creds():

    global val
    username = "acm-%i" % val
    val+=1

    password = xp.generate_xkcdpassword(mywords, numwords=3)
    password = password.title().replace(" ", "")

    return username, password


def load_data(filename):

    def student_exists(fsuid):
        return Student.query.filter_by(fsuid=fsuid).first() is not None

    def try_add(db, student):
        try:
            db.session.add(student)
            db.session.commit()
            print "Added student %s" % student
        except Exception as e:
            print "Error: %s" % e

    data = []
    map = dict()

    with open(filename, "r") as f:
        reader = csv.reader(f)
        reader.next() # strip dummy row
        data = [row for row in reader]

    # Generate initial students
    for row in data:
        student = Student(fsuid=row[4], first=row[1],
            last=row[2], email=row[3])
        if not student_exists(row[4]):
            try_add(db, student)
            map[str(student.fsuid)] = data.index(row)

    # # Add dummy students
    # for row in data:
    #     for id in row[6:8]:
    #         student = Student(fsuid=id)
    #         if not student_exists(id):
    #             try_add(db, student)

    # Generate teams
    for student in Student.query.all():
        row = data[map[str(student.fsuid)]]

        # If our primary-class students do not have a team...
        if student.team is None:

            # Make a team!
            u, p = get_creds()
            team = Team(team_name=str(row[5]) or "Unnamed Team", username=u, password=p)
            student.team = team
            db.session.add(team)
            db.session.commit()

            # Find their teammates, or create them.
            for id in row[6:8]:
                if id is None:
                    continue
                student = Student.query.filter_by(fsuid=id).first()
                if student is None:
                    student = Student(fsuid=id)
                    try_add(db, student)
                student.team = team




if __name__ == '__main__':
    load_data("data.csv")
