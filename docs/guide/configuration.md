# Configuration

::: tip IMPORTANT
The `.env` file does not interact with the Flask configurations and need to be configured separately.
:::

## Docker Compose and `.env`

::: warning CONFIGURING HOSTNAMES
See [this section](/guide/deployment.html#domains-and-subdomains) in Deployment on selecting domain/host names.
:::

The Compose config defines services for the project including:

  - Databases
  - Registration Webapp
  - Domjudge Server
  - Judgehosts
  - Nginx Proxies

Services are configured with their own volumes, ports, dependencies, and environment variables. The project currently uses Compose file version 2, whose docs can be found [here](https://docs.docker.com/compose/compose-file/compose-file-v2/).

We use the `.env` file to define several variables which control the project itself. Environmental variables from the `.env` file are interpolated into the 	`docker-compose.yml` using `${VAR}` syntax.

#### Example
#### `.env`
``` bash
VHOST=bastion.cs.fsu.edu
```
#### `docker-compose.yml`
``` yaml
# Registration webapp service
webapp:
  # ...
  environment:
    - FLASK_CONFIG=/webapp/config/production.py
    - VIRTUAL_HOST=${VHOST}
    - LETSENCRYPT_HOST=${VHOST}
    - LETSENCRYPT_EMAIL=andrew@fsu.acm.org
```



## Flask Config

The webapp's config is handled via setting an environmental variable `FLASK_CONFIG` to a file path relative to the webapp module's `__init__.py`. By default, these configs are to be stored in the repo's `/config` folder. Below is a sample config, but you can find the recommened developer config stored in `/config`. For production config, please contact project maintainers.

``` python
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
