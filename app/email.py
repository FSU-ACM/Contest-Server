from flask_mail import Message
from app import app, mail
from threading import Thread

# Async send message
def send_async_mail(app, msg):
    with app.app_context():
        mail.send(msg)

# Main reset functionality
def reset_password_email(address, password):

    msg = Message("Spring Programming Contest - Password Reset", sender="acm@cs.fsu.edu")
    msg.add_recipient(address)
    msg.body = "Here's your new password: %s. " % password
    msg.body += "Please consider setting a new password once you log back in."
    msg.body += "\n\nRegards,\nACM at FSU"

    # mail.send(msg)
    thr = Thread(target=send_async_mail, args=[app, msg])
    thr.start()

# Sign in functionality
def sign_in_email(address, domuser, dompass):

    msg = Message("Spring Programming Contest - Domjudge Credentials", sender="acm@cs.fsu.edu")
    msg.add_recipient(address)
    msg.body = "Here's your Domjudge credentials: \n\n"
    msg.body += "Username: {0} \n".format(domuser)
    msg.body += "Password: {0} \n".format(dompass)
    msg.body += "\n"
    msg.body += "Log in at domjudge.springprogrammingcontest.com.\n"
    msg.body += "\nRegards,\nACM at FSU"

    # mail.send(msg)
    thr = Thread(target=send_async_mail, args=[app, msg])
    thr.start()
