import os
import random
import string
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_mongoengine import MongoEngine, MongoEngineSessionInterface
from flask_nav.elements import *
from flask_recaptcha import ReCaptcha
from flask_admin import Admin

# Init & Config
app = Flask(__name__)
app.config.from_envvar('FLASK_CONFIG')
app.secret_key = ''.join(random.SystemRandom().choice(string.hexdigits) for _ in range(30))

# Init modules
bootstrap = Bootstrap(app)
db = MongoEngine(app)
recaptcha = ReCaptcha(app=app)
mail = Mail(app)

# Other Config
app.url_map.strict_slashes = False
app.session_interface = MongoEngineSessionInterface(db)

# Cache busting
@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)


def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                     endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)


from . import util, views, models

# Admin interface
admin = Admin(app, name='Admin Interface', template_mode='bootstrap3', index_view=views.admin.HomeView())

admin.add_view(views.admin.AccountManageView(models.Account))
admin.add_view(views.admin.TeamManageView(models.Team))
