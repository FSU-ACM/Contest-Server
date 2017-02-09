from flask import redirect, url_for, render_template, request
from flask_nav import Nav
from flask_nav.elements import *

import bleach, re

from app import app, recaptcha
from app.models import *
from signin import sign_in


# Email validator
EMAIL_REGEX = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")

# Nav bar
topbar = Navbar('',
    Link('Home', '/'),
	Link('Preregister', '/preregister'),
    Link('About', '/#about')
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
    success = None

    #Getting information from formi
    if request.method =='POST':
        name = bleach.clean(request.form['name'])
        email = bleach.clean(request.form['email'])

        # Verify recaptcha
        if not recaptcha.verify():
            error = "Please complete the ReCaptcha."

        # Check valid Email
        elif not EMAIL_REGEX.match(email):
            error = "Please submit a valid email."

        # Check unique email
        elif not Preregistration.query.filter_by(email=email).first():
            #Creating entry and inserting it into the database
            entry = Preregistration(email,name)
            db.session.add(entry)
            db.session.commit()
            #return render_template('prereg_land.html',email=email,name=name)
            success = """Congratulations, {}, you are now preregistered for the contest! We'll contact you at your email ({}) when full registration opens.""".format(name,email)
       	else:
            error = "This email is already registered."

    return render_template('prereg.html',error=error,success=success)
