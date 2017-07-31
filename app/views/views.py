from flask import redirect, url_for, render_template, request, session, abort

from app import app, recaptcha, db
from app.models import Account, Preregistration, Profile, Team
from app.util.email import reset_password_email
from app.util.password import reset_password as reset_pass
from app.util.views.auth import *

from datetime import date,datetime
import bleach, re


# Routes



# @app.route('/extracreditsurvey', methods=['POST','GET'])
# def extracreditsurvey():
#     error=None
#     success=None
#     allcourses=None
#     selectedcourses=None
#
#     action, profile = verify_profile(session)
#     print action, profile
#     action = None if not profile else redirect(url_for('profile',
#         message="Please login first"))
#
#     # get all courses from the databse for extra credit and store it in allcourses
#     # allcourses = ???
#
#     if request.method =='POST':
#         if 'courses' in request.form:
#             selectedcourses = bleach.clean(request.form['ec_courses'])
#
#         # save these courses for the extra credit survey associated with the profile
#
#         success = "Your courses were saved successfully"
#
#     return render_template('extracreditsurvey.html',error=error,success=success,
#         allcourses=allcourses, selectedcourses=selectedcourses)
