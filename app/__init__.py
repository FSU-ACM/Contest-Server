from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_recaptcha import ReCaptcha
from flask_nav import Nav
from flask_nav.elements import *

# Init & Config
app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')
app.config.from_pyfile('config.py')

# Init modules
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
recaptcha = ReCaptcha(app=app)

# Other Config
app.url_map.strict_slashes = False


from app import views
