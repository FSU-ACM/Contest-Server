from flask_mail import Message
from app import app, mail
from threading import Thread


# Async send message
def send_async_mail(app, msg):
    with app.app_context():
        mail.send(msg)


# Main reset functionality
def reset_password_email(address, password):
    msg = Message("ACM Programming Contest - Password Reset", sender="acm@cs.fsu.edu")
    msg.add_recipient(address)
    msg.body = "Here's your new password: %s. " % password
    msg.body += "Please consider setting a new password once you log back in."
    msg.body += "\n\nRegards,\nACM at FSU"

    # mail.send(msg)
    thr = Thread(target=send_async_mail, args=[app, msg])
    thr.start()


# Sign in functionality
def sign_in_email(address, domuser, dompass):
    msg = Message("ACM Programming Contest - Domjudge Credentials", sender="acm@cs.fsu.edu")
    msg.add_recipient(address)
    msg.body = "Here's your Domjudge credentials: \n\n"
    msg.body += "Username: {0}-{1} \n".format('team', domuser.split('-')[1].zfill(3))
    msg.body += "Password: {0} \n".format(dompass)
    msg.body += "\n"
    msg.body += "Log in at bastion.cs.fsu.edu.\n"
    msg.body += "\nRegards,\nACM at FSU"

    # mail.send(msg)
    thr = Thread(target=send_async_mail, args=[app, msg])
    thr.start()


# Quick registration support
def quick_register_email(address, password):
    msg = Message("ACM Programming Contest - Your Password", sender="acm@cs.fsu.edu")
    msg.add_recipient(address)
    msg.body = "Hello! Thanks for registering for the contest.\n\n"
    msg.body += "You can log in at bastion.cs.fsu.edu/login. "
    msg.body += "Here's your password: %s. " % password
    msg.body += "Please consider setting a new password once you log. \n\n"
    msg.body += "Once you log in, you can edit your profile and modify your team. You will need to remember your email so you can use it to sign in on the day of the contest.\n\n"
    msg.body += "If you think you're getting this email as an error, let us know at hello@acmatsfu.org.\n\n"
    msg.body += "Regards,\nACM at FSU"

    # mail.send(msg)
    thr = Thread(target=send_async_mail, args=[app, msg])
    thr.start()
