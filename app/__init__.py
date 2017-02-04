from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_nav import Nav
from flask_nav.elements import *

# Init
app = Flask(__name__)
bootstrap = Bootstrap(app)

# Config
app.url_map.strict_slashes = False

# DB Config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///storage/contest.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

from app import views
