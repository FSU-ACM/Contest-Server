""" Default configurations which ship with this project.
    For production, use another file (e.g. production.py) and import the
    :DefaultConfig: as the config base. """

import random
import string

class Config:
    """ Base configuration class. Exists because type-hinting DefaultConfig in the
        app factory method seemed weird. """


class DefaultConfig(Config):
    """ Default configuration for the project. Extend and override values from
        this config depending on your use-case. """

    DEBUG = False
    SECRET_KEY = ''.join(random.SystemRandom().choice(string.hexdigits) for _ in range(30))

    # Default amount of teams to generate
    TEAM_COUNT = 300

    # MongoDB Settinsg
    #MONGODB_DB = 'contest-server'
    MONGODB_HOST = 'mongodb://db/contest-server'

    # Email Configuration
    MAIL_SERVER = 'mail2.cs.fsu.edu'
    MAIL_PORT = '587'
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_DEFAULT_SENDER = 'acm@cs.fsu.edu'
    MAIL_USERNAME = 'acm'
    MAIL_PASSWORD = 'Override me in another config!'


    """ The following config options are currently unused, but shown
        below for future reference. """

    # ReCaptcha
    RECAPTCHA_ENABLED = False
    RECAPTCHA_SITE_KEY = '6LeyxBQUAAAAAHBpG2htNplW1qjcgODp47P6FHuE'
    RECAPTCHA_SECRET_KEY = 'Get the key from an officer!'

    # Basic Auth Creds
    BASIC_AUTH_USERNAME = 'acm'
    BASIC_AUTH_PASSWORD = 'acm'


class DevConfig(DefaultConfig):
    """ This is the default development config. Do not commit changes
        to this config. """

    DEBUG = True
    TEAM_COUNT = 20
    MONGODB_HOST = 'mongodb://localhost/contest-server'
    MAIL_PASSWORD = 'Get the password from an officer!'


class TestConfig(DefaultConfig):
    """ Testing configuration. """

    TEST = True
    DEBUG = True
    TEAM_COUNT = 5
    MONGODB_HOST = 'mongodb://localhost/contest-server-test'
