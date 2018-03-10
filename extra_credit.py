#!/usr/bin/env python
# Usage: python extra_credit.py <results.tsv>

from app.models import Team
import csv
import click


@click.command()
@click.argument('results_tsv', type=click.File('r'))
@click.argument('courses_csv', type=click.File('r'))
@click.argument('output_folder', type=str)
def extra_credit(results_tsv, courses_csv, output_folder):
    team_scores, user_scores = dict(), dict()
    student_classes = dict()
    class_files = dict()
    names = dict()

    # Read the score for each team
    tsv = csv.reader(results_tsv, delimiter='\t')
    next(tsv)
    for row in tsv:  # skip header line
        teamid, solved = row[0], row[3]
        team_scores[teamid] = solved

    # Match competitors with questions solved
    for teamid, score in team_scores.items():
        team = Team.objects(teamID=teamid).first()
        if not team.members:
            continue
        for account in team.members:
            if not account.signin:
                continue

            fsuid = account.email   # fallback is email
            if account.profile and account.profile.fsuid:
                # try and pull their fsuid from profile
                fsuid = account.profile.fsuid

            # Handles two situations:
            #   - no profile, so maybe we can autodetect FSUID from email
            #   - user is an idiot and put their fsu email in the 'fsuid' field
            if 'my.fsu.edu' in fsuid:
                fsuid = fsuid.lower().split('@')[0]

            user_scores[fsuid] = team_scores[teamid]

            if account.profile:
                names[fsuid] = account.profile.firstname, account.profile.lastname

    # Get student classes
    courses = csv.reader(courses_csv)
    next(courses)
    for row in courses: # skip header line
        fsuid, course_list = row[1], row[2]
        fsuid = fsuid.lower().split('@')[0]
        course_list = course_list.split(';')
        student_classes[fsuid] = course_list

    # Iterate over all students, retrieving their score from the
    # user_score dict and append "fsuid, score" to the course file
    def open_class_file(c):
        fd = open('{}/{}.csv'.format(output_folder, c), 'w')
        csv_writer = csv.writer(fd)
        return csv_writer

    for fsuid, course_list in student_classes.items():
        # FSUIDs from the survey not in the EC get None
        score = user_scores.get(fsuid, None)

        for course in course_list:
            if course not in class_files.keys():
                class_files[course] = open_class_file(course)
            first, last = names.get(fsuid, (None, None))
            class_files[course].writerow([fsuid, last, first, score])


    # If you completed the survey but didn't complete the profile, your score is None,
    # but you appear in the class file. Now we generate a file of identifiers in our
    # user_score that didn't show up in the survey, which will usually be people's
    # emails for those who did not complete the profile and didn't get their FSUID
    # auto-id'ed from a my.fsu.edu email address.

    orphans = set(user_scores.keys()) - set(student_classes.keys())
    orphan_csv = open_class_file('orphans')
    for orphan in list(orphans):
        score = user_scores.get(orphan, None)
        orphan_csv.writerow([orphan, score])


if __name__ == '__main__':
    extra_credit() #pylint: disable=E1120
