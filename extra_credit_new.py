#!/usr/bin/env python
# Usage: python extra_credit.py <results.tsv> <courses.csv>

"""
Output files explained:

-   If a student has a number at the end of their line, it means they
    competed in this division, and earned that score.
-   If a student has 0, it means they either didn’t compete in that
    division, or didn’t solve any questions.
-   If an fsuid doesn’t have a score, firstname, or last name, it
    means they completed the survey but did not show up to the contest
    (or made some sort of mistake while registering)

orphans.csv explained at the bottom.
"""

from app.models import Team, Account, Course
import csv
import click


@click.command()
@click.argument('results_tsv', type=click.File('r'))
@click.argument('output_folder', type=str)
@click.argument('division', type=int)
def extra_credit(results_tsv, output_folder, division):
    team_scores, user_scores = dict(), dict()
    student_classes = dict()
    class_files = dict()
    names = dict()

    def format_fsuid(account):
        # Try and grab fsuid or email
        fsuid = account.fsuid or account.email

        #  See if user is an idiot and put their fsu email in the 'fsuid' field
        if 'my.fsu.edu' in fsuid:
            fsuid = fsuid.split('@')[0]

        # Make extra sure fsuids from accounts are lower case (see issue #37)
        return fsuid.lower()

    # Read the score for each team
    print("Reading results_tsv...")
    tsv = csv.reader(results_tsv, delimiter='\t')
    next(tsv)
    for row in tsv:  # skip header line
        teamid, solved = row[0], row[3]
        team_scores[teamid] = solved

    # Match competitors with questions solved
    print("Matching teams to scores...")
    for teamid, score in team_scores.items():
        team = Team.objects(teamID=teamid).first()
        if not (team and team.members):
            continue
        for account in team.members:
            if not account.signin:
                continue

            fsuid = format_fsuid(account)

            user_scores[fsuid] = team_scores[teamid]

            names[fsuid] = account.first_name, account.last_name

    # Get student classes
    print("Reading extra credit survey...")

    def open_class_file(c):
        name = str(c).replace(' ', '_').replace('/', '_')
        fd = open('{}/{}.csv'.format(output_folder, name), 'w')
        csv_writer = csv.writer(fd)
        return csv_writer

    courses = Course.objects.all()

    for course in courses:
        students = Account.objects(courses=course)

        course_students = []

        for student in students:
            fsuid = format_fsuid(student)
            score = user_scores.get(fsuid, '0')
            first, last = names.get(fsuid, ('', ''))

            if type(score) != str:
                score = '0'
            
            if not student.team or student.team.division != division:
                continue

            course_students.append((fsuid, last, first, score,))

        if len(course_students) > 0:
            course_file = open_class_file(course)
            for s in sorted(course_students, key=lambda x: x[1]):
                course_file.writerow(s)

    # Put all students in 'all_students.csv'
    all_students = []
    students = Account.objects.all()
    for student in students:
        fsuid = format_fsuid(student)
        score = user_scores.get(fsuid, '0')
        first, last = names.get(fsuid, ('', ''))

        if type(score) != str:
            score = '0'
        
        if not student.team or student.team.division != division:
            continue

        all_students.append((fsuid, last, first, score,))

    
    all_students_file = open_class_file('all_students')
    for s in sorted(all_students, key=lambda x: x[1]):
        print(s)
        all_students_file.writerow(s)


if __name__ == '__main__':
    extra_credit() #pylint: disable=E1120
