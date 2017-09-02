#!/usr/bin/python

# What you have to do is pass the subject, the html, and an optional images folder as arguements
# and it will send an email with the images, and the html to everyone in the preregister database

# The way you add images to your html is by using <img src="cid:(namewithout.jpg)">
# Also there can not be two images of different types with the same extension

import sys
import os
import re
import smtplib

from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.utils import COMMASPACE, formatdate

sys.path.append('../..')

EMAIL_USERNAME = 'acm'
EMAIL_PASSWORD = 'zP4aCEm^'


if len(sys.argv) < 3 or len(sys.argv) > 4:
	print (sys.argv[0] + " <subject> <htmltosend> (imagefolder optional)")
	sys.exit(1)
dirname = sys.argv[3] if sys.argv[3][-1] == '/' else (sys.argv[3] + '/')
subject = sys.argv[1]
try:
	f = open(sys.argv[2], "r")
except IOError:
	print ("Could not open file!")
	sys.exit(2)
html = f.read()
f.close()

from app.models.Preregistration import *

emails = []
commaspace = ', '	

for instance in Preregistration.query:
    emails.append(instance.email)

fromaddr = 'acm@cs.fsu.edu'

msg = MIMEMultipart('related')
msg['From'] = fromaddr
msg['To'] = commaspace.join(emails)
msg['Date'] = formatdate(localtime=True)
msg['Subject'] = subject

msgAlternative = MIMEMultipart('alternative')
msgAlternative.attach(MIMEText(html, 'html'))

msg.attach(msgAlternative)

if len(sys.argv) == 4:
	for f in os.listdir(sys.argv[3]):
		if re.match(r'.*\.(jpg|png|gif|bmp)', f):
					image = open(dirname + f, 'rb')
					msgImage = MIMEImage(image.read())
					image.close()
					msgImage.add_header('Content-ID', '<' + os.path.splitext(f)[0] + '>')
					msg.attach(msgImage)


server = smtplib.SMTP('mail2.cs.fsu.edu:587')
server.starttls()
server.ehlo()
server.login(EMAIL_USERNAME, EMAIL_PASSWORD)
server.sendmail(fromaddr, emails, msg.as_string())
server.quit()
print ('Mail sent successfully')