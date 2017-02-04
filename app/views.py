from flask import redirect, url_for, render_template, request
from flask_nav import Nav
from flask_nav.elements import *

from app import app
from app.models import *
from signin import sign_in

# Nav bar
topbar = Navbar('SPC2017',
	Link('Sponsors', '/sponsors'),
	Link('Register', '/register'),
)

nav = Nav()
nav.register_element('top', topbar)
nav.init_app(app)



# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send/<string:fsuid>')
def send_mail(fsuid):
    addr = sign_in(fsuid)
    # if addr is not None:
    #     print fsuid, addr
    #     return redirect(url_for('confirm', addr=addr))
    # else:
    #     return render_template('walkin.html')
    return render_template('confirm.html', email=addr)

@app.route('/teams')
def teams():
    teams = Team.query.all()
    return render_template('teams.html', teams=teams)
