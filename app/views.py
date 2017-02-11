from flask import redirect, url_for, render_template, request
from flask_nav import Nav
from flask_nav.elements import *

import bleach, re

from app import app, recaptcha, db
from app.models.Preregistration import Preregistration
from signin import sign_in


# Email validator
EMAIL_REGEX = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")

# Nav bar
topbar = Navbar('SPC2017',
    Link('Home', '/'),
	Link('Preregister', '/preregister'),
	Link('Login','/login'),
	Link('Sign up','/signup')
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

@app.route('/login',methods=['POST','GET'])
def login():

    error = None
    success = None

    #Getting information from formi
    if request.method =='POST':
        email = bleach.clean(request.form['email'])
        password = bleach.clean(request.form['password'])

        # Verify recaptcha
        if not recaptcha.verify():
            error = "Please complete the ReCaptcha."

        # Check valid Email
        elif not EMAIL_REGEX.match(email):
            error = "Please submit a valid email."

        # verify that the password is not empty	
        elif not password:
            error = "Please enter a valid password."
			
        # Check unique email
        elif Preregistration.query.filter_by(email=email).first():
            #Creating entry and inserting it into the database
            entry = Login(email,password)
            db.session.add(entry)
            db.session.commit()
            #return render_template('prereg_land.html',email=email,name=name)
            success = """Congratulations, {}, you are now preregistered for the contest! We'll contact you at your email ({}) when full registration opens.""".format(name,email)
        else:
            error = "This email is not registered."

    return render_template('login.html',error=error,success=success)

@app.route('/signup',methods=['POST','GET'])
def signup():

    error = None
    success = None

    #Getting information from formi
    if request.method =='POST':
        firstname = bleach.clean(request.form['firstname'])
        lastname = bleach.clean(request.form['lastname'])
        age = bleach.clean(request.form['age'])
        gender = bleach.clean(request.form['gender'])
        race = bleach.clean(request.form['race'])
        degree = bleach.clean(request.form['degree'])
        major = bleach.clean(request.form['major'])
        advcourses = bleach.clean(request.form['advcourses'])
        email = bleach.clean(request.form['email'])
        password = bleach.clean(request.form['password'])

        error = verifyuserdetails(firstname, lastname, age, gender, race, degree, major, password)	
        # verify that user has entered all the required information	
        if error :
		    pass
			
        # Verify recaptcha
        elif not recaptcha.verify():
            error = "Please complete the ReCaptcha."

        # Check valid Email
        elif not EMAIL_REGEX.match(email):
            error = "Please submit a valid email."
			
        # Check unique email
        elif not Preregistration.query.filter_by(email=email).first():
            #Creating entry and inserting it into the database
            entry = Login(firstname,lastname,age,gender,degree,email,name)
            db.session.add(entry)
            db.session.commit()
            #return render_template('prereg_land.html',email=email,name=name)
            success = """Congratulations, {}, you are now preregistered for the contest! We'll contact you at your email ({}) when full registration opens.""".format(name,email)
        else:
            error = "This email is already registered."

    return render_template('signup.html',error=error,success=success)	
	
def verifyuserdetails(firstname, lastname, age, gender, race, degree, major, password):
    error = ""
    if not firstname:
        error += "Please enter a valid first name."	
		
    if not lastname:
        error += "Please enter a valid last name.\n"	

    if not age:
        error += "Please enter a valid age.\n"

    if not gender:
        error += "Please select a gender.\n"	

    if not race:
        error += "Please select a race.\n"
        
    if not degree:
        error += "Please enter a valid degree.\n"	

    if not major:
        error += "Please enter a valid major.\n"			

    if not password:
        error += "Please enter a valid password."	

	return error	