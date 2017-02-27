import sys

if len(sys.argv) is not 2:
    print "usage: ./createTeamCredentials target"
    exit()

# Run this script from ACM-Contest directory
# sys.path.append('../..')

from xkcdpass import xkcd_password as xp
from app.models import Team

def create(target):

    # Wind up
    wordfile = xp.locate_wordfile()
    mywords = xp.generate_wordlist(wordfile=wordfile, min_length=3, max_length=5)

    # Easy wrapper
    def password():
        words = xp.generate_xkcdpassword(mywords, numwords=3).split()
        words = [s.capitalize() for s in words]
        return ''.join(words)


    # Don't overwrite teams
    start = Team.objects.count()
    diff = target - start

    for i in range(start, target):
        teamID = "acm-%i" % i
        teamPass = password()
        domPass = password()

        Team(teamID=teamID, teamPass=teamPass, domPass=domPass).save()


if __name__ == '__main__':


    target = int(sys.argv[1])
    print "Generating up to %i teams." % target

    create(target)
