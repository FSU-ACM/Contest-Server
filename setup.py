#!/bin/sh

# Make sure all depts are up to date
npm install
pip install -r requirements.txt

# Build non-source files
# gulp sass
# ^^ doesn't work for some reason

# Generate teama
python app/scripts/createTeamCredentials.py 500 
