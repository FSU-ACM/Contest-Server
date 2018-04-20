# Introduction

This project consists of several discrete software components, which are as follows:

  - Registration Webapp
  - Domjudge Contest Server
  - Domjudge Judgehosts
  - MongoDB & MariaDB databases
  - Nginx Reverse Proxies

All of the components of the project are deployed using Docker. Docker is a tool which containerizes software into small, light-weight virtual machines. Each of our primary components are deployed in their own Docker container.

Theses docs focus primarily on the Flask webapp for User/Team Registration, but details for deploying Domjudge can be found in the [Deployment](#deployment) section below. The repository for those Docker images can be found [here](https://github.com/FSU-ACM/Docker-Domjudge).


## Features

  - User & Team Registration
    - Quick Registration of an entire team
    - Solo registration for individual participants
    - Team management features (add/remove members, rename)
  - Domjudge Integration
    - Simple deployment of Domserver & Judgehosts with Docker
    - Easy scaling of Judgehost instances
  - Networking
    - Simple domain/subdomain support via `jwilder/nginx-proxy` imagej
    - Automatic free SSL certificates from LetsEncrypt

::: tip
See the `docker-compose.yml` for the environmental variables related to the [nginx-proxy image](https://github.com/jwilder/nginx-proxy).
:::


## How it Works

### Registration Webapp
The webapp is written in Python 3 (previously Python 2) using the Flask web microframework. Flask allows Python to act as an interactive web server which can dynamically render webpage templates, manage user sessions via secure cookies, and integrate with additional libraries to extend functionality. Some of the libraries we use include:

  - MongoEngine: A Object Document Manager which provides an API to the MongoDB database.
  - WTForms: A form creation and validation framework.
  - Jinja 2: A templating language bundled with Flask.
  - Node.js: A Javascript runtime environment.
  - Sass: A preprocessed stylesheet language.

The webapp depends on the `db` service in the Docker Compose config which runs the MongoDB database.

### Domjudge
DOMjudge is an automated judging system for running programming contests such as ACM's ICPC. Domjudge comes in two components: the Domserver and the Judgehosts.

Deploying the Domjudge components with Docker has several key advantages:

  - Script complex installation process via Dockerfile
  - Easily scale and redeploy Judgehosts

``` bash
# Scaling judgehosts
docker-compose scale judgehost=4
```

The Domsserver depends on the `domdb` service in the Docker Compose config which runs the MariaDB database.

### Nginx
To provide networking to Domserver and the Registration webapp, we employ a few instances of Nginx.

The first is the publicly available image [`jwilder/nginx-proxy`](https://github.com/jwilder/nginx-proxy). This image can forward traffic for different domains and subdomains to other containers on the same Docker Compose project network by setting environmental variables for those services in the Docker Compose configuration file.

The [`jwilder/nginx-proxy`](https://github.com/jwilder/nginx-proxy) image has a companion image, [`JrCs/letsencrypt-nginx-proxy-companion`](https://github.com/JrCs/docker-letsencrypt-nginx-proxy-companions) which can automatically register the domains with LetsEncrypt to create free SSL certificates for the domains.

::: tip
Those image names are also links.
:::



## To Do
A comprehensive list of to-do items is available on this project's [Github Issues page](https://github.com/fsu-acm/contest-server/issues).

