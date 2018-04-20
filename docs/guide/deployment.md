# Deployment

Deploying this project should be as simple as the steps [on the home page](/#easy-to-deploy), but in practice the suite can be much more finicky. Here we'll cover the details of deployment and steps to take to correct common problems.

## In a Perfect World...

If there were no issues, all it should take are the following steps:

``` bash
# Download the code
git clone https://github.com/FSU-ACM/Contest-Server.git

# Import the config
cp /path/to/prod/.env ./.env
cp /path/to/flask/prod/config ./config

# Build the images
docker-compose build

# Deploy the suite
docker-compose up
```

That probably won't work. In fact, we recommend not using `docker-compose up` to launch all services, but to bring up the services individually in this order:

  1. Nginx Proxy
  2. Databases
  3. Servers
  4. Judgehosts

You can launch the services individually using:
``` bash
# Relevant flags: -d (detatch), --build
docker-compose up [flags] [service]
```

## Domains and Subdomains
In [this section](/guide/configuration.html#docker-compose-and-env) of the [Configuration docs](/guide/configuration.html), we discuss configuring the software using environmental variables. Part of the configuration process is setting up the `nginx-proxy` service with our hostnames for the webapp and domserver.

When deploying, you need to make sure whatever DNS settings exist for your domain names point to the IP of the host server this project is deployed to.

#### Example
For ACM at FSU's Spring 2018 contest, we deployed this project to the `bastion.cs.fsu.edu` server. The `bastion.cs.fsu.edu` domain name was already configured by FSU to point to the server, so we set the `VHOST` env variable to `bastion.cs.fsu.edu` for the `webapp` service. Likewise, we did the same for `contest.acmatfsu.org` to the `Domserver` service.

::: danger
There are some problems accessing the `acmatfsu.org` domain from the C.S. department network. Contact project maintainers for addition details.
:::

## Common Issues

### Boot Order
The Docker Compose configuration uses the `depends_on` settings to try and control the boot order. We do this because the servers can't launch without their respective databases. However, even with the databases launching beforehand, they might not be ready to receive connections by the time the servers come online.

The Domserver has an explicitly defined loop to retry the MariaDB database until it's ready, but the webapp's behavior from MongoEngine is not explicitly known to this project's maintainers at the time of writing this.

::: warning jwilder/nginx-proxy
The Docker Compose project uses the [`jwilder/nginx-proxy`](https://github.com/jwilder/nginx-proxy) image for networking between the Docker containers. As of Spring 2018, this image has some issues detecting new containers as they come online and occasionally requires a host reboot to function properly.
:::

