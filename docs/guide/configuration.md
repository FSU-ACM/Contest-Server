# Configuration

This page describes how to configure:

  1. The Flask user/team registration webapp
  2. The Docker Compose project

These configurations are two seperate files, both of which need to be created in order for this suite to run properly. This page has sample/starter examples for both configurations, which you can copy into your files for development and/or deployment.

::: tip IMPORTANT
The `.env` file does not interact with the Flask configurations and need to be configured separately.
:::

## Docker Compose and `.env`

The Compose config defines services for the project including:

  - Databases
  - Registration Webapp
  - Domjudge Server
  - Judgehosts

Services are configured with their own volumes, ports, dependencies, and environment variables. The project currently uses Compose file version 2, whose docs can be found [here](https://docs.docker.com/compose/compose-file/compose-file-v2/).

We use the `.env` file to define several variables which control the Compose configuration. Environmental variables from the `.env` file are interpolated into the 	`docker-compose.yml` using `${VAR}` syntax.

#### Sample `.env`
``` bash
COMPOSE_PROJECT_NAME=contest
DOM_PASS=abadpassword
```
#### Excerpt from `docker-compose.yml`
``` yaml
# Registration webapp service
domserver:
  # ...
  environment:
    - DOMJUDGE_DB_HOST=domdb
    - DOMJUDGE_DB_PASSWORD=${DOM_PASS}
    - DOMJUDGE_DB_ROOT_PASSWORD=${DOM_PASS}
```
#### Output of `docker-compose config`
``` yaml
domserver:
  # ...
  environment:
    DOMJUDGE_DB_HOST: domdb
    DOMJUDGE_DB_PASSWORD: abadpassword
    DOMJUDGE_DB_ROOT_PASSWORD: abadpassword
```

## Flask Configuration

The webapp's config is handled via setting an environmental variable `FLASK_CONFIG` to a file path relative to the webapp module's `__init__.py`. By default, these configs are to be stored in the repo's `/config` folder. Below is a sample config, but you can find the recommened developer config stored in `/config`. For production config, please contact project maintainers.

``` python
# General dev config
DEBUG = True

# MongoDB
MONGODB_SETTINGS = {
  'db': 'database',         # name of the database in MongoDB
  'host': 'localhost',      # hostname of server
  'port': 27017,
  'username': 'username',   # Database user
  'password': 'password',   # User's password
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
MAIL_USERNAME = '<ACM USERNAME>'
MAIL_PASSWORD = '<ACM PASSWORD>'

```
