""" Various things that need to run with the app context at launch """

import os
from flask import Flask, url_for
from flask_bootstrap import Bootstrap
from flask_mongoengine import MongoEngine, MongoEngineSessionInterface
from flask_recaptcha import ReCaptcha
from app.models import Team

# pylint: disable=W0105,W0612
def setup(app: Flask, db: MongoEngine):

    # Non-config configuration stuff
    app.url_map.strict_slashes = False
    app.session_interface = MongoEngineSessionInterface(db)

    # Initialize external libraries
    Bootstrap(app)
    ReCaptcha(app)

    # Cache busting
    @app.context_processor
    def override_url_for():
        def dated_url_for(endpoint, **values):
            if endpoint == "static":
                filename = values.get("filename", None)
                if filename:
                    file_path = os.path.join(app.root_path, endpoint, filename)
                    values["q"] = int(os.stat(file_path).st_mtime)
            return url_for(endpoint, **values)
        return dict(url_for=dated_url_for)

    # Flash filters
    @app.template_filter('alert')
    def map_flash_category(category: str):
        return {
            'success': 'success',
            'message': 'info',
            'error': 'danger',
        }.get(category)

    # Pre-generate teams
    @app.before_first_request
    def generate_teams():
        if Team.objects.count() < app.config["TEAM_COUNT"]:
            from app.util.password import make_password

            # Don't overwrite teams
            start = 1 + Team.objects.count()
            target = 1 + app.config["TEAM_COUNT"]

            """
            Domjudge doesn't support acm-0 (0 is not a valid ID), so
            whenever we start generating acm-x we use +1. Hence, to reach 300
            teams we must generate acm-1 through acm-301.

            This still does not solve the issue if a team is removed in the middle.
            This should be rewritten to start at the largest existing team ID.
            """

            for i in range(start, target):
                team_id = "acm-%i" % i
                team_pass = make_password()
                dom_pass = make_password()

                Team(teamID=team_id, teamPass=team_pass, domPass=dom_pass).save()
