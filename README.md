# Programming Contest Server Suite
> All-inclusive suite for running ACM at FSU's Fall/Spring Programming Contests

This project is composed of primary components: the user/team management systems, and the Domjudge contest judging system. Also included are Nginx reverse-proxies and Docker to it all together.

This README focuses primarily on the Flask webapp for User/Team Registration, but details for deploying Domjudge can be found in the [Deployment](#deployment) section below. The repository for those Docker iamges can be found [here](https://github.com/FSU-ACM/Docker-Domjudge).


## Getting Started
This section will explain how to set up the project on your machine for development/testing.

### Prerequisites
This project relies heavily on [Docker](https://docs.docker.com/) and [Docker Compose](https://docs.docker.com/compose/). While not _strictly required_ for development, it is _highly recommended_.

The registration webapp uses [MongoDB](https://www.mongodb.com/) as the database. You can either [install MongoDB](https://docs.mongodb.com/manual/installation/) on your host machine or deploy a MongoDB container inside Docker using this project's Docker Compose config.

This project also has some dependency on [Node.js](https://nodejs.org/en/), [npm](https://www.npmjs.com/)/[Yarn](https://yarnpkg.com/), [Gulp](https://gulpjs.com/), and [Sass](http://sass-lang.com/) for managing/building styles. Currently the project includes pre-built stylesheets, but if you wish to recomplile them you will need these dependencies.

### Installation
#### Python Dependencies
To manage the dependencies of the webapp, we _strongly recommend_ using a [virtualenv](https://virtualenv.pypa.io/en/stable/). You may also be interested in [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/).

Install Python the requirements:
```
> pip install -r requirements.txt
```

#### Node.js Dependencies
Install the Node.js dependencies:
```sh
# Yarn method
> yarn		# install arg not required

# npm method
> npm i		# i === install
```
We recommend Yarn over npm (it's faster!).

You also probably want to install Gulp globally.
```sh
# Yarn
> yarn global add gulp

# npm
> npm i -g gulp
```

### Running the webapp
Once everything is installed (and your MongoDB instance is running), you must specify a config via environmental variable to launch the server. The config path is relative to the main `__init__.py`.

Specify config and launch in one line:
```sh
> FLASK_CONFIG=../config/development.py python start.py
```
If you have the Node.js deps installed, you can:
```sh
# Yarn method
> yarn dev

# npm method
> npm run dev
```


## Deployment
The docker-compose project uses the `nginx-proxy` image for networking between the Docker containers. As of Spring 2018, this image has some issues and occasionally requires a host reboot to function properly.

You can launch the whhole docker-compose project using:
```
docker-compose up
```
However, this is not recommended. We recommend first bringing up the database services [`db`, `domdb`], then the `nginx-proxy` and companion services, then the web servers [`webapp`, `domserver`]. Later, the `judgehost` instances.

#### Judgehosts
Judgehosts should be launched separately from the rest of the suite, as they are prone to crashing. Be sure to provide them with the correct domain address, or attach them to the suite's Docker network and set the hostname accordingly.



## Misc. Details
### Configuration
The webapp's config is handled via setting an environmental variable `FLASK_CONFIG` to a file path relative to the webapp module's `__init__.py`. By default, these configs are to be stored in the repo's `./config` folder. Below is a sample config, but you can find the recommened developer config stored in `./config`. For production config, please contact project maintainers.

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
MAIL_USERNAME = None
MAIL_PASSWORD = None

```

These config values override the basic config values from the root's
`/config.py` file

### Styles
This project uses Sass to define the styles. Sass needs to be pre-compiled into CSS before the image is built. In Development mode, when Sass rebuilds the changes are automatically updated in the app. However, if you are making changes outside of development mode, run `gulp` to rebuild the Sass styles.

For setting up Gulp and Sass:
```
npm install
npm install -g gulp
```
Be sure to install npm beforehand.




### Code Style

#### Python `import` statements
Import statements in python files should follow a certain pattern. Imports should be performed in this order:

1. Imports from Flask or Flask extension packages.
2. Imports from app modules
3. Imports from the python standard library.

If there are multiple lines of imports from a section, there should be empty lines above and below that section. For long lines, use `( )` to wrap imports. Imports should be alphabetically ordered in all possible contexts.

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

from flask import (redirect, render_template, request, session,
	url_for, )

from app import app, basic_auth
from app.email import sign_in_email
from app.models import Account, Profile, Team
from app.util.auth import verify_email

import datetime, re
```
