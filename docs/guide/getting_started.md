# Getting Started
This section will explain how to set up the project on your machine for development/testing.

## Prerequisites
This project relies heavily on [Docker](https://docs.docker.com/) and [Docker Compose](https://docs.docker.com/compose/). While not _strictly required_ for development, it is _highly recommended_.

The registration webapp uses [MongoDB](https://www.mongodb.com/) as the database. You can either [install MongoDB](https://docs.mongodb.com/manual/installation/) on your host machine or deploy a MongoDB container inside Docker using this project's Docker Compose config.

This project also has some dependency on [Node.js](https://nodejs.org/en/), [npm](https://www.npmjs.com/)/[Yarn](https://yarnpkg.com/), [Gulp](https://gulpjs.com/), and [Sass](http://sass-lang.com/) for managing/building styles. Currently the project includes pre-built stylesheets, but if you wish to recomplile them you will need these dependencies.

## Installation
#### Python Dependencies
To manage the dependencies of the webapp, we _strongly recommend_ using a [virtualenv](https://virtualenv.pypa.io/en/stable/). You may also be interested in [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/).

Install Python the requirements:
``` bash
pip install -r requirements.txt
```

#### Node.js Dependencies
For building the Sass, install the dependencies from `package.json`:
``` bash
# Yarn method
yarn    # install arg not required

# npm method
npm i	# i === install
```

::: tip
We recommend Yarn over npm (it's faster!).
:::


## Running the webapp
Once everything is installed (and your MongoDB instance is running), you must specify a config via environmental variable to launch the server. The config path is relative to the main `__init__.py`.

Specify config and launch in one line:
``` bash
FLASK_CONFIG=../config/development.py python start.py
```

::: tip
Be sure your config is right before launching. You can the config docs [here](/guide/configuration.html).
:::


If you have the Node.js deps installed, you can:
``` bash
# Yarn method
yarn dev

# npm method
npm run dev
```

## Contributing
Before making changes, be sure to read our [Contributing Guidelines](/contributing/) to make sure your changes stay within our recommended practices.
