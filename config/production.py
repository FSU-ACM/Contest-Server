# Default production config
DEBUG = False

TEAM_COUNT = 500

# MongoDB
MONGODB_SETTINGS = {
	'db': 'fpc2017',	# "project"
	'host': 'db', 		# "127.0.0.1"
	'port': 27017, 		# 27017
    # 'username': None, # 'username'
    # 'password': None, # 'passwd'
}

# ReCaptcha
RECAPTCHA_ENABLED = True
RECAPTCHA_SITE_KEY = '6LeyxBQUAAAAAHBpG2htNplW1qjcgODp47P6FHuE'
RECAPTCHA_SECRET_KEY = ''

# Email Config
MAIL_SERVER = 'mail.cs.fsu.edu'
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USE_SSL = False
MAIL_DEFAULT_SENDER = 'acm@cs.fsu.edu'
MAIL_USERNAME = None
MAIL_PASSWORD = None

# Basic Auth Creds
# BASIC_AUTH_USERNAME = ''
# BASIC_AUTH_PASSWORD = ''
