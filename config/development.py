# Default production config
DEBUG = True

TEAM_COUNT = 20

# MongoDB
MONGODB_SETTINGS = {
	'db': "fpc2017",	# "project"
	'host': "db", 		# "127.0.0.1"
	'port': 27017, 		# 27017
    # 'username': "None", # 'username'
    # 'password': None, # 'passwd'
}

# ReCaptcha
RECAPTCHA_ENABLED = False
RECAPTCHA_SITE_KEY = '6LeyxBQUAAAAAHBpG2htNplW1qjcgODp47P6FHuE'
RECAPTCHA_SECRET_KEY = ''

# Email Config
MAIL_SERVER = 'mail2.cs.fsu.edu'
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USE_SSL = False
MAIL_DEFAULT_SENDER = 'acm@cs.fsu.edu'
MAIL_USERNAME = 'acm'
MAIL_PASSWORD = '1017Academic!Way'

# Basic Auth Creds
# BASIC_AUTH_USERNAME = ''
# BASIC_AUTH_PASSWORD = ''
