from flask import Flask

from .models import db
from .util.email import mail
from .util.setup import setup
from .views import init_app as init_views


def create_app(config: str = "config.default.DefaultConfig") -> Flask:
    """ Factory method for the flask app. Returns an instance of the app.

        :param config: Instance of a Config object"""

    app = Flask(__name__)
    app.config.from_object(config)

    # Configure app
    db.init_app(app)
    mail.init_app(app)

    # Initialize misc. app functions
    setup(app, db)

    # Add the views
    init_views(app)

    return app
