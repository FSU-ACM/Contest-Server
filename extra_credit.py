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

    # Read the score for each team
    tsv = csv.reader(results_tsv, delimiter='\t')
    next(tsv)
    for row in tsv:  # skip header line
        teamid, solved = row[0], row[3]
        team_scores[teamid] = solved

    # Match competitors with questions solved
    for teamid, score in team_scores.iteritems():
        team = Team.objects(teamID=teamid).first()
        if not team.members:
            continue
        for account in team.members:
            if not account.profile or not account.profile.fsuid or not account.signin:
                continue
            fsuid = account.profile.fsuid
            user_scores[fsuid] = team_scores[teamid]

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

    for fsuid, course_list in student_classes.iteritems():
        # FSUIDs from the survey not in the EC data don't appear.
        score = user_scores.get(fsuid, None)

        for course in course_list:
            if course not in class_files.keys():
                class_files[course] = open_class_file(course)
            if score is not None:
                class_files[course].writerow([fsuid, score])


if __name__ == '__main__':
    extra_credit()
