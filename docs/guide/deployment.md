# Deployment

Deploying this project should be as simple as the steps [on the home page](/#easy-to-deploy), but in practice the suite can be much more finicky. Here we'll cover the details of deployment and steps to take to correct common problems.

## In a Perfect World...

If you're deploying on a server whose Nginx configuration is already complete, redeploying the services should be as easily as follows (otherwise see [Deploying with Nginx](#deploying-with-nginx)):

``` bash
# Download the code
git clone https://github.com/FSU-ACM/Contest-Server.git

# Copy in your config
cp /your/docker/.env ./.env
cp /your/flask/production.py ./config/production.py

# Build the images
docker-compose build

# Deploy the suite
docker-compose up -d
```

If that doesn't work, you try can starting services individually in the following order. Where there are failures, consult the logs using `docker-compose logs -f <service>`.

  1. Databases
  2. Servers
  3. Judgehosts

You can launch the services individually using:
``` bash
# Relevant flags: -d (detatch), --build
docker-compose up [flags] <service>
```

## Deploying with Nginx
On the Bastion server, we use Nginx to provide reverse proxying (connecting incoming web connections made to `bastion.cs.fsu.edu` to the correct service). Nginx requires configuration before use. Here's a rough overview of how to configure Nginx for deployment:

### Make sure Nginx is installed
There are many guides for installing Nginx on a Linux server. Here's an abbreviated version:

```sh
sudo apt-get update
sudo apt-get install -y nginx
```

### Add the Bastion Nginx configuration
In the repository, an Nginx configuration is saved at `/config/nginx/bastion.conf`. You should copy this into the Nginx configuration directory, probably located at `/etc/nginx/sites-available`.

You also need to link the configuration so it's "enabled":

```sh
ln -s /etc/nginx/sites-available/bastion.conf /etc/nginx/sites-enabled/
```

You should also remove any other configurations in `sites-enabled/` unless you really know what you're doing.

### Configure HTTPS/SSL using Certbot
Once the configuration is installed and linked, you should be able to access the webapp from `http://bastion.cs.fsu.edu`. Now follow the official Cerbot directions [here](https://certbot.eff.org/lets-encrypt/ubuntuxenial-nginx) to install Certbot and configure the domains.

### Summary
Once all is done, you will have configured SSL connections for the Webapp and Domserver services. This means that external connections on port 443 will be forwarded via HTTP (not HTTPS) to the servers running inside docker containers in their locally exposed ports.

## Common Issues

### Boot Order
The Docker Compose configuration uses the `depends_on` settings to try and control the boot order. We do this because the servers can't launch without their respective databases. However, even with the databases launching beforehand, they might not be ready to receive connections by the time the servers come online.

The Domserver has an explicitly defined loop to retry the MariaDB database until it becomes ready. However, the Flask webapp's behavior in the MongoEngine connection is not explicitly known to this project's maintainers at the time of writing this.
