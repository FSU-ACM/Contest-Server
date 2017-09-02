#!/bin/bash
''''
export PYTHONPATH=`pwd`/../..
python $0
exit 0
'''

from app.models.Team import *

for team in Team.query.all():
	print team.csv()
