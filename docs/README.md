---
home: true
heroImage: /logo.png
actionText: Read the Docs →
actionLink: /guide/
features:
  - title: User Management
    details: Comprehensive team management via Flask webapp.
  - title: Domjudge Integration
    details: Easily deploy Domjudge alongside the registration system.
  - title: Plug-n-play
    details: Very easy to deploy. Add your configuration and launch.
footer: MIT Licensed | Copyright © 2018-present ACM at FSU
---

### Easy to deploy
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
::: tip WELL, NOT SO FAST...
See the [deployment guide](/guide/deployment) for more details on launching the suite.
:::
