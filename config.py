# Default production config
DEBUG = False

# SQLAlchemy
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_DATABASE_URI = None              # Must be overridden with /instance

# MongoDB
MONGODB_SETTINGS = {
	'db': None,	# "project"
	'host': None, # "127.0.0.1"
	'port': None, # 12345
    'username': None, # 'username'
    'password': None, # 'passwd'
}

# ReCaptcha
RECAPTCHA_ENABLED = True
RECAPTCHA_SITE_KEY = '6LeyxBQUAAAAAHBpG2htNplW1qjcgODp47P6FHuE'
RECAPTCHA_SECRET_KEY = ''
