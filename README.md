# Contest Server Suite
> All-inclusive suite for running ACM at FSU's Fall/Spring Programming Contests

https://fsu-acm.github.io/Contest-Server

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

## Built With
  - [Flask](http://flask.pocoo.org/) – Python webapp framework.
  - [Bulma](https://bulma.io/) – CSS Flexbox framework.
  - [Sass](https://sass-lang.com/) – Preprocessed CSS stylesheet.
  - [npm](https://npmjs.com) – The package manager for javascript.
  - Docker – Software containerization.
  - Nginx – Reverse proxy server.

## Contributing
Contributions are welcome! Please read both the [Getting Started](https://fsu-acm.github.io/Contest-Server/guide/getting_started.html) guide and the [Contributing Guidelines](https://fsu-acm.github.io/Contest-Server/contributing) before submitting changes.

## Versioning
We use something similar to [SemVer](https://semver.org/). Incrementation is not derived from API changes, but from significant adjustment to codebase:

  - MAJOR version for significant codebase rewrites.
  - MINOR version for localized changes, e.g. adding a new feature.
  - PATCH version for any adjustment to `master` codebase, e.g. bugfix.

## Authors
  - Andrew Sosa – _Initial work_ – [andrewsosa](https://github.com/andrewsosa)

See also the list of [contributors](https://github.com/fsu-acm/Contest-Server/contributors) who participated in this project.

## License
MIT
