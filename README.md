# Contest-Suite
Flask suite for running Fall/Spring Programming Contests

Here is the requirements documents:
https://docs.google.com/document/d/1_9VTQSOmZ_X8lVzaUFmRy_2ldRHsIqK-1720amgIq0U/edit?usp=sharing

## Developing and Deployment
This suite uses Docker for both development and deployment. You will need to
install both [Docker](https://www.docker.com/community-edition) and
[Docker Compose](https://docs.docker.com/compose/install/).

Once both are installed, you can launch the suite in development mode using:
```
docker-compose -f .docker/development.yml up -d
```

For deployment, use `.docker/production.yml` instead.

### Styles
This project uses Sass to define the styles. Sass needs to be pre-compiled into
CSS before the image is built. In Development mode, when Sass rebuilds the
changes are automatically updated in the app. However, if you are making
changes outside of development mode, run `gulp` to rebuild the Sass styles.

For setting up Gulp and Sass:
```
npm install
npm install -g gulp
```
Be sure to install npm beforehand. 


## Configuration
Configuration is handled by creating a `/instance` folder in the project's
root directory. Inside, create a file `config.py` in which to declare
the required variables. Below is a sample configuration.

```
# General dev config
DEBUG = True

# MongoDB
MONGODB_SETTINGS = {
	'db':   'database',	# name of the database in MongoDB
	'host': 'localhost', 	# hostname of server
	'port': 27017,
    'username': 'username',	# Database user
    'password': 'password',	# User's password
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

```

These config values override the basic config values from the root's
`/config.py` file


## Code Style

### File headers
Each non-init python file should begin with a comment labeling its contents
with respect to package scope.

For example, `app/views/admin/sign_in.py` should be commented:
```python
# views.admin.sign_in

```

### Python `import` statements
Import statements in python files should follow a certain pattern. Imports
should be performed in this order:

1. Imports from Flask or Flask extension packages.
2. Imports from app modules
3. Imports from the python standard library.

If there are multiple lines of imports from a section, there should be empty
lines above and below that section.

#### Example 1
```python
# from views._util.auth

from flask import redirect, url_for
from app.models import Profile
import re

```

#### Example 2
```python
# from views.admin.sign_in

from flask import redirect, url_for, render_template, request, session

from app import app, basic_auth
from app.models import Account, Profile, Team
from app.email import sign_in_email
from app.util.views.auth import verify_email

import datetime, re

```


## Mail handling
todo
