from app.models import *
import smtplib

from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate



msg = 'This is a triumph! Making a note here, great success.'

DOMJUDGE_ADDRS = "http://52.24.58.195/domjudge"
EMAIL_USERNAME = 'acm'
EMAIL_PASSWORD = 'zP4aCEm^'

def get_email(fsuid):

    # Grab the student, dummy or full.
    student = Student.query.filter_by(fsuid=fsuid).first() or None

    # Let's see if we have an entry
    if student is not None:

        # This student filled out the form
        if student.email is not None:
            return student.email

        # This student did not
        else:
            team = student.team
            for teammate in team.students:
                if teammate.email is not None:
                    return teammate.email
            return None

    # No entry, fallback
    else:
        return None

def get_domjudge_creds(fsuid):

    # Grab the student, dummy or full.
    student = Student.query.filter_by(fsuid=fsuid).one()
    team = student.team
    return team.username, team.password


def send_email(toaddr, msg_text):

        fromaddr = "acm@cs.fsu.edu"


        msg = MIMEMultipart()
        msg['From'] = fromaddr
        msg['To'] = toaddr
        msg['Date'] = formatdate(localtime=True)
        msg['Subject'] = "ACM Contest Credentials"

        msg.attach(MIMEText(msg_text))

        server = smtplib.SMTP('mail2.cs.fsu.edu:587')
        server.starttls()
        server.login(EMAIL_USERNAME, EMAIL_PASSWORD)
        #toaddr = "andrewsosa001@gmail.com"
        server.sendmail(fromaddr, toaddr, msg.as_string())
        server.quit()
        print 'sent mail succcessfully to %s' % toaddr



def sign_in(fsuid):

    # Record that someone entered the FSUID
    si = SignIn(fsuid=fsuid)
    db.session.add(si)
    db.session.commit()
    print "Recorded Sign-in of %s" % fsuid

    # fromaddr = 'acm@cs.fsu.edu'
    toaddr = get_email(fsuid)   # email lookup

    if toaddr is None:
        return None

    username, password = get_domjudge_creds(fsuid)  # credentials

    text = """
        Here are your credentials to login to the contest.
        Web Address: {0}
        Username: {1}
        Password: {2}

        Please let an ACM officer know if there are any problems with
        your credentials.
        """.format(DOMJUDGE_ADDRS, username, password)


    if toaddr is not None:
        send_email(toaddr, text)
        return toaddr
    else:
        return None, username, password
