from app.models import *
import sys

for team in Team.query.all():
    print team.csv(include_students=len(sys.argv)>1)
