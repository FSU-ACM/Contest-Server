# views.register.quick_register

from flask import redirect, url_for, render_template, request, session

from app import app, recaptcha
from app.forms import QuickRegister as QuickRegisterForm
from app.models import Account, Team
from app.util import auth2, session as session_util
from app.util.auth import verify_email
from app.util.team import *
from app.util.password import make_password
from app.util.email import quick_register_email
from app.util.auth import get_account
from app.views.generic import FormView

import bleach


class QuickRegisterView(FormView):
    """

    """

    def authorize(self):
        return not session_util.is_auth()

    def redirect_unauthorized(self):
        flash("You are already registered!", 'message')
        return redirect(url_for('profile'))

    def get_template_name(self):
        return 'form2/quick_register.html'

    def get_form(self):
        return QuickRegisterForm()

    def post(self):
        form = QuickRegisterForm(request.form)

        if form.validate():

            accounts = []

            # Create account 1
            pass1 = make_password()
            account1 = auth2.create_account(
                email=form.email1.data,
                password=pass1,
                first_name=form.first_name1.data,
                last_name=form.last_name1.data,
                fsuid=form.fsuid1.data
            )
            quick_register_email(account1.email, pass1)
            accounts.append(account1)

            # Account 2
            if form.account2:
                pass2 = make_password()
                account2 = auth2.create_account(
                    email=form.email2.data,
                    password=pass2,
                    first_name=form.first_name2.data,
                    last_name=form.last_name2.data,
                    fsuid=form.fsuid2.data
                )
                quick_register_email(account2.email, pass2)
                accounts.append(account2)

            # Account 3
            if form.account3:
                pass3 = make_password()
                account3 = auth2.create_account(
                    email=form.email2.data,
                    password=pass3,
                    first_name=form.first_name3.data,
                    last_name=form.last_name3.data,
                    fsuid=form.fsuid3.data
                )
                quick_register_email(account3, pass3)
                accounts.append(account3)

            # Create team
            first, team = True, None
            while len(accounts) > 0:
                account = accounts.pop(0)
                if first:
                    team = create_team(account, form.team_name.data)
                    set_division(team, form.division.data)
                    first = False
                else:
                    join_team(account, team=team)

            flash('Team created! Please check your emails for your passwords.', 'success')
            return redirect(url_for('login'))

        return self.render_template(form=form)


# @app.route('/quickregister', methods=['GET'])
# def quick_register():
#     error = request.args.get('error', None)
#     success = request.args.get('success', None)

#     # Disuade double registering
#     action, account = get_account(session)
#     action = None if not account else redirect(url_for('profile',
#                                                        message="You are already registered!"))

#     if not action:
#         action = render_template('/form/quick_register.html', error=error, success=success)

#     return action


# @app.route('/quickregister', methods=['POST'])
# def quick_register_post():
#     error, success = None, None

#     form = request.form.to_dict()

#     # Collect details
#     name = form.get('teamname', None)
#     division = form.get('division', None)
#     emails = [
#         bleach.clean(form.get('email1', None)),
#         bleach.clean(form.get('email2', None)),
#         bleach.clean(form.get('email3', None))
#     ]
#     emails = [e for e in emails if e is not None]
#     emails = [e for e in emails if e != ""]
#     accounts = []

#     # Make sure this is done
#     if not recaptcha.verify():
#         error = "Please complete the ReCaptcha."

#     # Make sure and division are provided
#     if not error:
#         if not name or not division:
#             error = "Please provide your team and division with atleast one email."
#     name = bleach.clean(name)

#     # Verify all emails
#     if not error:
#         for email in emails:
#             if not verify_email(email):
#                 console.log(email)
#                 error = "Please submit valid emails."
#                 break

#     # Make sure these emails do not have accounts
#     if not error:
#         for email in emails:
#             if Account.objects(email=email).first():
#                 error = "%s is already registered." % email

#     # If no validation errors...
#     if not error:

#         # Create accounts
#         for email in emails:
#             account = Account(email=email)
#             password = make_password()
#             account.set_password(password)
#             account.save()
#             quick_register_email(account.email, password)
#             accounts.append(account)

#         # Put on team, send email
#         first = True
#         team = None
#         while len(accounts) > 0:
#             account = accounts.pop(0)
#             if first:
#                 team = create_team(account, name)
#                 set_division(team, division)
#                 first = False
#             else:
#                 error, x = join_team(account, team=team)
#             if error:
#                 break

#     action = None
#     if error:
#         action = redirect(url_for('quick_register', error=error))
#     else:
#         action = redirect(url_for('login', success="Check your email for your password!"))

#     return action
