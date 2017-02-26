#!/bin/sh

# Make sure all depts are up to date
npm install
pip install -r requirements.txt

# Build non-source files
gulp sass

# Restart hosting
if [ -z ${CONTEST_SERVICE} ]; then
	echo "CONTEST_SERVICE is unset, did not restart service."
else
    systemctl restart $CONTEST_SERVICE
    systemctl status $CONTEST_SERVICE
fi
