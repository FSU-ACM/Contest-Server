from flask import redirect, url_for, render_template, request, session, abort

from app import app, recaptcha, db
from app.models import Account, Preregistration, Profile, Team
from app.util.email import reset_password_email
from app.util.password import reset_password as reset_pass
from app.views._util.auth import *

from datetime import date,datetime
import bleach, re


# Routes


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
        elif not verify_email(email):
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

    # # Shadowban?
    # if profile is not None and profile.shadowban is True:
    #     abort(404)

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
        team.teamName = team.teamName[:Team.MAX_NAME_LENGTH]

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

            # # Shadowban?
            # if team.shadowban is True:
            #     abort(404)

            team.teamName = request.form['teamName'] or "Unnamed Team"
            team.teamName = team.teamName[:Team.MAX_NAME_LENGTH]
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

@app.route('/extracreditsurvey', methods=['POST','GET'])
def extracreditsurvey():
    error=None
    success=success
    allcourses=None
    selectedcourses=None

    action, profile = verify_profile(session)
    print action, profile
    action = None if not profile else redirect(url_for('profile',
        message="Please login first"))

    # get all courses from the databse for extra credit and store it in allcourses
    # allcourses = ???

    if request.method =='POST':
        if 'courses' in request.form:
            selectedcourses = bleach.clean(request.form['ec_courses'])

        # save these courses for the extra credit survey associated with the profile

        success = "Your courses were saved successfully"

    return render_template('extracreditsurvey.html',error=error,success=success,
        allcourses=allcourses, selectedcourses=selectedcourses)


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
