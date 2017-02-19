from flask import redirect, url_for, render_template, request, session
from flask_nav import Nav
from flask_nav.elements import *
from datetime import date,datetime


import bleach, re

from app import app, recaptcha, db
# from app.models.Preregistration import Preregistration
from app.models import Account, Preregistration, Profile, Team
from signin import sign_in


# Email validator
EMAIL_REGEX = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")

# Nav bar
topbar = Navbar('',
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
        elif not Preregistration.objects(email=email).first():
            #Creating entry and inserting it into the database
            prereg = Preregistration(email=email,name=name)
            prereg.save()
            success = """Congratulations, {}, you are now preregistered for the contest! We'll contact you at your email ({}) when full registration opens.""".format(name,email)

        else:
            error = "This email is already registered."

    return render_template('prereg.html',error=error,success=success)

@app.route('/login',methods=['POST','GET'])
def login():

    error = None
    success = None
    insertrecaptcha = False

    # Activate recaptcha if too many bad attempts
    if 'counter' in session and session['counter'] >= 3:
        insertrecaptcha = True


    # Getting information from form
    if request.method =='POST':
        email = bleach.clean(request.form['email'])
        password = bleach.clean(request.form['password'])

        # Check valid Email
        if not EMAIL_REGEX.match(email):
            error = "Please submit a valid email."
        # verify that the password is not empty
        elif not password:
            error = "Please enter a valid password."
        # If we needed recaptcha, make sure they have it
        elif insertrecaptcha and not recaptcha.verify():
            error = "Please complete the ReCaptcha."

        # Check accounts if we don't have an error yet
        if error is None:

            account = Account.objects(email=email).first()
            correctpwd = account.check_password(password) if account else False

            # SUCCESS
            if account and correctpwd:
                session['email']=email
                return redirect('/profile', code=302)
            # FAILURE : Incorrect Password
            elif account and not correctpwd:
                #If login fails 3rd time and beyond, make user enter recaptcha
                session['counter']=session.get('counter',0)+1
                if session['counter'] >= 3:
                    insertrecaptcha = True # Turn reCaptcha in login on
                    error = "You have made too many incorrect login attempts. Please verify that you are not a robot."
                else:
                    error = "Invalid password."
            # FAILURE : Email not registered.
            else:
                error = "This email is not registered."

    return render_template('login.html',error=error, success=success, insertrecaptcha=insertrecaptcha)

@app.route('/profile', methods=['POST','GET'])
def profile():

    error = None
    success = None
    email = None


    # check if the user is logged in. If not, rturn to the login page
    if 'email' not in session:
         return redirect(url_for('login'))
    else:
        email = session['email']


    # Get the account stuff
    account = Account.objects(email=email).first()
    profile = account.profile

    #Getting information from form
    if request.method =='POST':

        # Extract important data from form
        data = dict()
        for k,v in request.form.iteritems():
            data[k] = bleach.clean(v)

        # Special case to get race
        race = request.values.getlist('race')
        if len(race) > 0:
            data['race'] = race

        # Clean empty fields (TODO: make this unnessessary)
        to_delete = []
        for k,v in data.iteritems():
            if v is None or v == "":
                to_delete.append(k)
        for k in to_delete:
            print "Removed %s" % k
            del data[k]


        # Let's save our data.
        if profile:
            # update profile
            profile.update(**data)
            success = "Profile updated."
        else:
            profile = Profile(**data)
            account.profile = profile
            success = "Profile created."

        # Save and handle errors
        try:
            profile.save()
            account.save()
        except Exception as e:
            error =  "Hey, there's been an error! Sorry about that. "
            error += "Please email hello@acmatfsu.org and let us know. "
            error += "We'll try and get it sorted out ASAP."
            print e

    return render_template('profile.html',error=error,success=success,profile=profile)

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
        elif not Account.objects(email=email).first():
			# Create an account for our user
            account = Account(email=email)
            account.set_password(password)

			# Let's see if they preregistered
            prereg = Preregistration.objects(email=email).first()
            if prereg:
				account.prereg = prereg

            # DB transactions
            account.save()

            # Set cookie, redirect to profile page.
            session['email']=email
            return redirect('/profile', code=302)

        else:
            error = "This email is already linked to an another account."

    return render_template('register.html',error=error)

@app.route('/updatepassword', methods=['POST','GET'])
def updatepassword():
    error = None
    success = None

    # check if the user is logged in. If not, return to the login page
    if 'email' not in session:
        return redirect(url_for('login'))

    if request.method=='POST':
        email=session['email']
        currentpassword=request.form['currentpassword']
        newpassword=request.form['newpassword']

        # Check if the old password is corect
        account = Account.objects(email=email).first()
        if not account.check_password(currentpassword):
            error = "That's not your current password."
        elif newpassword == currentpassword:
            error = "New password cannot be same as the current password"
        else:
            account.set_password(newpassword)
            account.save()
            success = "Password updated successfully"

    return render_template('updatepassword.html',error=error,success=success)


@app.route('/logout', methods=['POST','GET'])
def logout():
    try:
        del session['email']
    except KeyError:
        pass

    return redirect("/",code=302)


def verifyuserdetails(firstname, lastname, dob, major, advProg, ifstudent):
    error = ""
    dob_date = None
    wrong_dob_format = False
    #dob_date = datetime.strptime(dob,"%Y-%m-%d")
    #Checking date format
    try:
        dob_date = datetime.strptime(dob,"%Y-%m-%d")
    except ValueError as err:
        print(err)
        wrong_dob_format = True
    if dob_date > datetime(2017,01,01) or dob_date < datetime(1890,01,01):
        wrong_dob_format = True

    if not firstname:
        error += "Please enter a valid first name."

    if not lastname:
        error += "Please enter a valid last name.\n"

    if not dob or wrong_dob_format:
        error += "Please enter a valid date of birth. Format yyyy-mm-dd.\n"

    if not major and ifstudent:
        error += "Please enter a valid major.\n"

    if not advProg and ifstudent:
        error += "Please select a valid most advanced program.\n"

    return error
