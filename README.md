# Contest-Suite
Flask suite for running Fall/Spring Programming Contests

Here is the requirements documents:
https://docs.google.com/document/d/1_9VTQSOmZ_X8lVzaUFmRy_2ldRHsIqK-1720amgIq0U/edit?usp=sharing


## Configuration
Configuration is handled by creating a `/instance` folder in the project's
root directory. Inside, create a file `config.py` in which to declare
the required variables. Below is a sample configuration.

```
# General dev config
DEBUG = True

# MongoDB
MONGODB_SETTINGS = {
	'db': 'database',		# name of the database in MongoDB
	'host': 'localhost', 	# hostname of server
	'port': 27017,
    'username': 'username', # Database user
    'password': 'password', # User's password
}

```

These config values override the basic config values from the root's
`/config.py` file
