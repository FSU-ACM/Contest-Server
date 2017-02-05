from flask import redirect, url_for, render_template, request
from flask_nav import Nav
from flask_nav.elements import *

from app import app
from app.models import *
from signin import sign_in

# Nav bar
topbar = Navbar('SPC2017',
    Link('Home', '/'),
	Link('Preregister', '/preregister'),
	# Link('Sponsors', '/#sponsors'),
    # Link('FAQ','/#faq')
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

@app.route('/preregister',methods=['POST','GET'])
def preregister():
    error = None
    #Getting information from formi
    if request.method =='POST':
        name = request.form['name']
        email = request.form['email']
        #Creating entry and inserting it into the database
        if not Preregistration.query.filter_by(email=email).first():
            entry = Preregistration(email,name)
            db.session.add(entry)
            db.session.commit()
            return render_template('prereg_land.html',email=email,name=name)
       	else:
                error = "Email already in list"
    return render_template('prereg.html',error=error)
