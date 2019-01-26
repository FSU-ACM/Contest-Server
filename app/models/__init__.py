# pylint: ignore=C0413
from flask_mongoengine import MongoEngine

db = MongoEngine()

from .Account import Account
from .Team import Team
