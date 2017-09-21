# views.account.profile

from flask import redirect, url_for, render_template, request, session, abort

from app import app
from app.models import Account, Profile
from app.util.auth import *

import bleach

@app.route('/account/profile', methods=['POST','GET'])
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

    if profile:
        # If there's a profile at this point, add it to the session
        session['profile_id'] = str(profile.id)
    else:
        # Set message for non-profile
        message = "Please provide your basic information before you proceed."

    return render_template('/form/profile.html',error=error,success=success,
        message=message, profile=profile)
