from flask import redirect, url_for, render_template, request, session, abort
from flask_nav import Nav
from flask_nav.elements import *
from datetime import date,datetime


import bleach, re

from app import app, recaptcha, db
# from app.models.Preregistration import Preregistration
from app.models import Account, Preregistration, Profile, Team
from email import reset_password_email
from password import reset_password as reset_pass


# Email validator
EMAIL_REGEX = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")

# Nav bar
nav_logged_in = Navbar('',
    Link('Home', '/'),
    Link('FAQ','/#faq'),
    Link('Sponsors', '/#sponsors'),
    # Link('Teams','/allteams'),
    Link('Profile','/profile'),
)

nav_logged_out = Navbar('',
    Link('Home', '/'),
    Link('FAQ','/#faq'),
    Link('Sponsors', '/#sponsors'),
    # Link('Teams','/allteams'),
    Link('Login','/login'),
)

nav = Nav()
nav.register_element('logged_in', nav_logged_in)
nav.register_element('logged_out', nav_logged_out)
nav.init_app(app)

# Auth tools
def verify_login(session):
    if 'email' not in session or 'profile_id' not in session:
          return redirect(url_for('login')), None, None
    else:
        return None, session['email'], session['profile_id']

def verify_profile(session):
    if 'profile_id' not in session:
        return redirect(url_for('profile',
            error="You need a profile to complete this action.")), None
    else:
        profile = Profile.objects.get_or_404(id=session['profile_id'])
        return None, profile

# Routes
@app.route('/')
def index():
    return render_template('index.html')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500


@app.route('/allteams')
def allteams():
    teams = Team.objects.filter(teamName__exists=True)
    return render_template('allteams.html', teams=teams)

# Route disabled
# @app.route('/preregister', methods=['POST','GET'])
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

    return render_template('/form/prereg.html',error=error,success=success)

@app.route('/login',methods=['POST','GET'])
def login():

    # maybe enable after checking security
    # if 'email' in session and 'profile_id' in session:
    #     return redirect('/profile', code=302)

    # error = request.args.get('error', None)
    error = request.args.get('error', None)
    success = request.args.get('success', None)
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
                return redirect(url_for('profile'), code=302)
            # FAILURE : Incorrect Password
            elif account and not correctpwd:
                #If login fails 3rd time and beyond, make user enter recaptcha
                session['counter']=session.get('counter',0)+1
                if session['counter'] >= 3:
                    insertrecaptcha = True # Turn reCaptcha in login on
                    error = "You have made too many incorrect login attempts. Please verify that you are not a robot."
                else:
                    error = "Invalid password."
            # FAILURE : Email not (register)ed.
            else:
                error = "This email is not registered."

    return render_template('/form/login.html',error=error, success=success, insertrecaptcha=insertrecaptcha)

@app.route('/profile', methods=['POST','GET'])
def profile():

    error = request.args.get('error', None)
    success = request.args.get('success', None)
    message = request.args.get('message', None)
    profile = None

    # check if the user is logged in. If not, rturn to the login page
    if 'email' not in session:
         return redirect(url_for('login', error="You are not logged in."))
    email = session['email']

    # Get the account stuff
    account = Account.objects(email=email).first()
    profile = account.profile

    #Getting information from form
    if request.method =='POST':

        # Extract important data from form
        data = dict()
        for k,v in request.form.iteritems():
            # add to dict only if there is a values
            v = bleach.clean(v)
            if v:
                data[k] = v

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
        else:
            profile = Profile(**data)
            account.profile = profile

        # Save and handle errors
        try:
            profile.save()
            account.save()
            success = "Profile updated."

        except Exception as e:
            error =  "Hey, there's been an error! Sorry about that. "
            error += "Please email hello@acmatfsu.org and let us know. "
            error += "We'll try and get it sorted out ASAP."
            print e

    # If there's a profile at this point, add it to the session
    if profile:
        session['profile_id'] = str(profile.id)

    return render_template('/form/profile.html',error=error,success=success,
        message=message, profile=profile)

@app.route('/register', methods=['POST','GET'])
def register():

    error = request.args.get('error', None)
    success = request.args.get('success', None)

    # Disuade from registering twice
    action, profile = verify_profile(session)
    print action, profile
    action = None if not profile else redirect(url_for('profile',
        message="You are already registered!"))

    if not action:

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

            elif not recaptcha.verify():
                error = "Please complete the ReCaptcha."

            # SUCCESS STATE
            elif not Account.objects(email=email).first():
                # Create an account for our user
                account = Account(email=email)
                account.set_password(password)

                # Let's see if they preregistered
                prereg = Preregistration.objects(email=email).first()
                account.prereg = prereg if prereg else None

                # DB transactions
                account.save()

                # Set cookie, redirect to profile page.
                session['email']=email
                action = redirect(url_for('profile'), code=302)

            else:
                error = "This email is already linked to an another account."

        action = action if action is not None else \
            render_template('/form/register.html',error=error)

    return action

@app.route('/updatepassword', methods=['POST','GET'])
def updatepassword():

    error, success = None, None

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

    return render_template('/form/updatepassword.html', error=error,success=success)


@app.route('/resetpassword', methods=['POST'])
def reset_password():

    error, success = None, None
    error_msg = "No such email on file."

    email = request.form['email']

    error = None if EMAIL_REGEX.match(email) else error_msg

    if not error:

        account = Account.objects(email=email).first()

        if account:
            reset_password_email(email, reset_pass(account))
            success = "Password email sent."
        else:
            error = error_msg

    return redirect(url_for('login', success=success, error=error))


@app.route('/logout', methods=['POST','GET'])
def logout():
    try:
        del session['email']
        del session['profile_id']
    except KeyError:
        pass

    return redirect(url_for('index'),code=302)

@app.route('/profile/team', methods=['GET'])
def team():
    """
    Here a user can either view their team details if
    on a team, otherwise have the options to create
    or join a team.
    """

    error = request.args.get('error', None)
    success = request.args.get('success', None)

    # Access profile (throws 404)
    action, profile = verify_profile(session)

    if not action:

        # Let's see if they have a team
        team = profile.team

        action = render_template('/form/profile_team.html', team=team,
            profile=profile, error=error, success=success)

    return action

@app.route('/profile/team', methods=['POST'])
def team_create():
    """
    This route is for creating a new team.
    """

    error, success = None, None

    # Access the profile (n/a throws 404)
    action, profile = verify_profile(session)

    # Make sure they're not already on a team
    action = None if (action is None and not profile.team) else action or \
        redirect(url_for('team', error="You're already on a team!"))

    # Given profile and no team:
    if not action:

        """
        ATTENTION:
        The following code is a workaround for a bug in MongoEngine.
        When removing the last element from a ListField and saving
        the document, it removes the field from the document.
        Therefore, we first look for teams without the field before
        finding ones with it missing.
        """


        # Let's assign them a team
        team = Team.objects.filter(members__exists=False).first()

        if team is None:
            team = Team.objects.filter(members__size=0).first()

        # More workaround code
        if team.members is None:
            team.members = [profile]
        else:
            team.members.append(profile)
        profile.team = team

        # Set the team name
        team.teamName = request.form['teamName'] or team.teamID

        # Safety first!
        try:
            team.save()
            profile.save()
        except:
            abort(500)

        action = redirect(url_for('team'))

    return action

@app.route('/profile/team/rename', methods=['POST'])
def team_update():
    """
    This route is for updating team names.
    """

    error, success = None, None

    # Access profile (n/a throws 404)
    action, profile = verify_profile(session)

    # Make sure they're on a team, but preserve an existing action
    action = None if (action is None and profile.team) else action or \
        redirect(url_for('team', error="You need to be on a team to do that!"))

    # Given profile and team, do:
    if not action:
        try:
            team = profile.team
            team.teamName = request.form['teamName'] or "Unnamed Team"
            team.save()
            sucess = "Team name updated."
        except:
            abort(500)

        action = redirect(url_for('team', success=sucess, error=error))

    return action

@app.route('/profile/team/join', methods=['POST'])
def team_join():
    """
    This route allows a user to join a team.
    """

    error, success = None, None

    # Access profile (n/a throws 404)
    action, profile = verify_profile(session)

    # Perform join if profile exists
    if not action:

        # Team lookup
        teamID, teamPass = request.form['teamID'], request.form['teamPasscode']
        team = Team.objects(teamID=teamID,teamPass=teamPass).first()

        if team:

            # Max 3 members
            if not team.members:
                team.members = [profile] # See workaround notice above
                team.save()
                profile.team = team
                profile.save()
                success = "You joined the team!"
            elif len(team.members) < 3:
                team.members.append(profile)
                profile.team = team
                team.save()
                profile.save()
                success = "You joined the team!"
            else:
                error = "Team %s already has 3 members." % \
                    team.teamName or team.teamID
        else:
            error = "Team with those credentials not found."

        action = redirect(url_for('team', success=success, error=error))

    return action

@app.route('/profile/team/leave', methods=['POST'])
def team_leave():
    """
    This route allows a user to leave their team.
    """

    error, success = None, None

    # Access profile (n/a throws 404)
    action, profile = verify_profile(session)

    # Green means go
    if not action:

        # Retrieve team
        team = profile.team

        # Attempt to leave
        try:
            profile.team = None
            profile.save()

            team.members.remove(profile)

            # Clear name if last member
            if len(team.members) is 0:
                team.members = []
                team.teamName = None
            team.save()

            success = "You have left the team."
        except Exception as e:
            print e
            abort(500)

        action = redirect(url_for('team', success=success, error=error))

    return action


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
