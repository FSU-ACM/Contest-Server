import csv
from collections import Counter

results = open("team-login-results.csv").readlines()
walkins = open("andrews-walkins.csv").readlines()

def get_row(file_, index):
    for line in file_:
        if line.split(",")[0] is index:
            return line
    return None

team_score = Counter()
individual_score = dict()

for line in results[1:]:
    team = line.split(",")[0]
    team_score[team] += 1

for line in walkins[1:]:
    for fsuid in line.split(",")[1:]:
        individual_score[fsuid.rstrip()] = team_score[line.split(",")[0]]

# for k,v in individual_score.iteritems():
#     print k,v

with open("walkin-results.csv", "w") as walkin_results:
    for id,score in individual_score.iteritems():
        walkin_results.write(id + "," + str(score) + "\n")
