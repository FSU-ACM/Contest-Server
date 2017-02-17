from flask import redirect, url_for, render_template, request, session
from flask_nav import Nav
from flask_nav.elements import *

import bleach, re

from app import app, recaptcha, db
# from app.models.Preregistration import Preregistration
from app.models import Account, Preregistration, Profile, Team
from signin import sign_in


# Email validator
EMAIL_REGEX = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")

# Nav bar
topbar = Navbar('SPC2017',
    Link('Home', '/'),
	Link('Register', '/register'),
	Link('Login','/login'),
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


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


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
    insertrecaptcha = False

    #Getting information from formi
    if request.method =='POST':
        email = bleach.clean(request.form['email'])
        password = bleach.clean(request.form['password'])

        # # Verify recaptcha
        # if not recaptcha.verify():
        #     error = "Please complete the ReCaptcha."

        # Check valid Email
        if not EMAIL_REGEX.match(email):
            error = "Please submit a valid email."

        # verify that the password is not empty
        elif not password:
            error = "Please enter a valid password."

        # Check unique email
        elif Preregistration.query.filter_by(email=email).first():

            # if login fails because of incorrecct password, increment the counter
            # variable in session object.
            #session['counter']=session.get('counter',0)+1

            #If login fails 3rd time and beyond, make user enter recaptcha
            # if session['counter'] >=3:
            #     insertrecaptcha  = True
            #     error = "You have made too many incorrct login attempts. Please verify that you are not a robot."
            # else:
            #     error = "Invalid password"
            # return render_template('login.html',error=error, success=success, insertrecaptcha = insertrecaptcha)

            #Creating entry and inserting it into the database
            entry = Login(email,password)
            db.session.add(entry)
            db.session.commit()
            session['email']=email
            return render_template('profile.html',error=error, success=success, insertrecaptcha = insertrecaptcha)
            #return render_template('prereg_land.html',email=email,name=name)
        else:
            error = "This email is not registered."

    return render_template('login.html',error=error,success=success)

@app.route('/profile', methods=['POST','GET'])
def profile():

    error = None
    success = None

    # check if the user is logged in. If not, rturn to the login page
    # if 'email' not in session:
    #     return redirect(url_for('login'))

    #Getting information from formi
    if request.method =='POST':
        firstname = bleach.clean(request.form['firstname'])
        lastname = bleach.clean(request.form['lastname'])
        fsuid = bleach.clean(request.form['fsuid'])
        dob = bleach.clean(request.form['dob'])
        gender = bleach.clean(request.form['gender'])
        race = None
        if 'race' in request.form:
            race = bleach.clean(request.form['race'])
        major = bleach.clean(request.form['major'])
        gradyear = bleach.clean(request.form['gradyear'])
        gradterm = bleach.clean(request.form['gradterm'])
        degree = None
        if 'degree' in request.form:
            degree = bleach.clean(request.form['degree'])
        advcourses = bleach.clean(request.form['advcourses'])
        foodallergies = bleach.clean(request.form['foodallergies'])
        email = session['email']

        # verify that user has entered all the required information
        error = verifyuserdetails(firstname, lastname, dob, major, advcourses)
        if error :
            pass

        # TODO fix this so it updates an existing user profile
        # Check unique email
        elif Preregistration.query.filter_by(email=email).first():
            #Creating entry and inserting it into the database
            entry = Profile(firstname,lastname,fsuid,dob,gender,race,major,gradyear,gradterm,degree,advcourses,foodallergies)
            db.session.add(entry)
            db.session.commit()
            #return render_template('prereg_land.html',email=email,name=name)
            success = "Profile updated successfully"
        else:
            error = "This email is not registered."

    return render_template('profile.html',error=error,success=success)


@app.route('/register', methods=['POST','GET'])
def register():

    error = None

    if request.method == 'POST':

        # Validate login; deny or redirect to profile
        email = bleach.clean(request.form['email'])
        password = bleach.clean(request.form['password'])

        # Validate email
        if not EMAIL_REGEX.match(email):
            error = "Please submit a valid email."

        # Validate password
        elif not password:
            error = "Please enter a valid password."

        # SUCCESS STATE
        elif not Account.query.filter_by(email=email).first():
			# Create an account for our user
            account = Account(email, password)

			# Let's see if they preregistered
            prereg = Preregistration.query.filter_by(email=email).first()
            if prereg:
                # Link for lulz
				account.prereg = prereg

            # DB transactions
            db.session.add(account)
            db.session.commit()

            # Set cookie, redirect to profile page.
            session['email']=email
            return redirect('/profile', code=302)

        else:
            error = "This email is already linked to an another account."

    return render_template('register.html',error=error)


def verifyuserdetails(firstname, lastname, dob, major, advcourses):
    error = ""
    if not firstname:
        error += "Please enter a valid first name."

    if not lastname:
        error += "Please enter a valid last name.\n"

    if not dob:
        error += "Please enter a valid date of birth.\n"

    if not major:
        error += "Please enter a valid major.\n"

    if not advcourses:
        error += "Please select a valid advancedcourses.\n"

    return error
