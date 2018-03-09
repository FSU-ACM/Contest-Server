# views.account.profile

from flask import flash, redirect, url_for, render_template, request, session, abort

from app import app
from app.forms import Profile as ProfileForm
from app.models import Account, Profile
from app.util import session as session_util
from app.views.generic import FormView, AccountFormView


import bleach, logging


class ProfileView(AccountFormView):
    """Collects extra data from user.

    Unauth'd users redirected to login.

    """

    def get_template_name(self):
        return 'form2/profile.html'

    def get_form(self):
        account = session_util.get_account()
        if account.profile:
            return ProfileForm(obj=account.profile)
        else:
            return ProfileForm()

    def post(self):
        form = ProfileForm(request.form)

        if form.validate():
            account = session_util.get_account()
            data = {field.name: field.data for field in form}
            for k,v in data.items():
                app.logger.debug("{} {}".format(k, v))
            del data['csrf_token']
            del data['submit']


            if not account.profile:
                account.profile = Profile(**data)
            else:
                account.profile.update(**data)

            account.profile.save()
            account.save()

            flash('Profile updated')

        return self.render_template(form=form)



# @app.route('/account/profile', methods=['POST', 'GET'])
# def profile():
#     error = request.args.get('error', None)
#     success = request.args.get('success', None)
#     message = request.args.get('message', None)
#     profile = None

#     # check if the user is logged in. If not, rturn to the login page
#     if 'email' not in session:
#         return redirect(url_for('login', error="You are not logged in."))
#     email = session['email']

#     # Get the account stuff
#     account = Account.objects(email=email).first()
#     profile = account.profile

#     # Getting information from form
#     if request.method == 'POST':

#         # Extract important data from form
#         data = dict()
#         for k, v in request.form.items():
#             # add to dict only if there is a values
#             v = bleach.clean(v)
#             if v:
#                 data[k] = v

#         # Special case to get race
#         race = request.values.getlist('race')
#         if len(race) > 0:
#             data['race'] = race

#         # Clean empty fields (TODO: make this unnessessary)
#         to_delete = []
#         for k, v in data.items():
#             if v is None or v == "":
#                 to_delete.append(k)
#         for k in to_delete:
#             del data[k]

#         # Let's save our data.
#         if profile:
#             # update profile
#             profile.update(**data)
#         else:
#             profile = Profile(**data)
#             account.profile = profile

#         # Save and handle errors
#         try:
#             profile.save()
#             account.save()
#             success = "Profile updated."

#         except Exception as e:
#             error = "Hey, there's been an error! Sorry about that. "
#             error += "Please email hello@acmatfsu.org and let us know. "
#             error += "We'll try and get it sorted out ASAP."
#             logging.error(e)

#     if profile:
#         # If there's a profile at this point, add it to the session
#         session['profile_id'] = str(profile.id)
#     else:
#         # Set message for non-profile
#         message = "Please provide your basic information before you proceed."

#     return render_template('/form/profile.html', error=error, success=success,
#                            message=message, profile=profile)
