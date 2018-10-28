---
sidebar: auto
---

# Contributing

Thanks for considering contributing to this project!

The following is a set of guidelines and best practices to follow while contributing to this project. If something is unclear, or there might be a better way to do things, feel free to propose changes to these guidelines in a pull request.

## Proposing Changes

### Git Flow
We prefer to use a lightweight version of the Git Flow paradigm. To contribute changes, fork the repository and follow these steps:

1. Update your `master` branch to the latest version of `fsu-acm/master`.
2. Create a new branch for your changes, `my-feature`, or `my-bugfix`.
3. Commit your changes to your working branch.
4. Push your branch to your remote repository, e.g. `andrewsosa001/my-bugfix`.
5. Open a PR from your remote branch to `fsu-acm/master`.
6. Once accepted, repeat from step s1.

::: tip
You can read a more detailed description of the Git Flow paradigm [here](https://gist.github.com/andrewsosa/77090b96d61b849c3fc3ecb974b6a568).
:::

### Git Commit Messages
When writing commit messages for your changes, do the following:

  - Use the present tense ("Add feature" not "Added feature")
  - Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
  - Limit the first line to 72 characters or less
  - Reference issues and pull requests liberally after the first line

### Versioning
We use something similar to [SemVer](https://semver.org/). Incrementation is not derived from API changes, but from significant adjustment to codebase:

  - MAJOR version for significant codebase rewrites.
  - MINOR version for localized changes, e.g. adding a new feature.
  - PATCH version for any adjustment to `master` codebase, e.g. bugfix.

### Things To Avoid
  - Commiting files not part of the project (e.g, `.DS_Store`)
  - Making unintentional changes to dependencies lists such as `requirements.txt` or `package.json`.
  - Updating files not explicitly related to your changes.

## Updating Webapp Styles

This project uses Sass to define the styles. Sass needs to be pre-compiled into CSS before the image is built. In Development mode, when Sass rebuilds the changes are automatically updated in the app. However, if you are making changes outside of development mode, run `gulp` to rebuild the Sass styles.

For setting up Gulp and Sass:
``` bash
# Install project deps
npm install

# Globally install gulp
npm install -g gulp
```

Alternatively, you can run a local version of `gulp` using `npx` instead of globally installing Gulp.

``` bash
# Uses gulp from node_modules
npx gulp
```

::: warning
Be sure to install `npm` beforehand.
:::


## Code Guidelines

For easy of maintainability, we prefer specific ways of writing across the project.

### PEP8
Please try to stick to [PEP8](https://www.python.org/dev/peps/pep-0008/) while writing Python code. We admit that the current codebase isn't strictly PEP8 already, but we can make it better over time!

...unless we contradict PEP8 in the following guidelines; in which case you probably should still follow PEP8 and tell us why we're doing it wrong.

### Python `import` statements
Import statements in python files should follow a certain pattern. Imports should be performed in this order:

1. Imports from Flask or Flask extension packages.
2. Imports from app modules
3. Imports from the python standard library.

If there are multiple lines of imports from a section, there should be empty lines above and below that section. For long lines, use `( )` to wrap imports. Imports should be alphabetically ordered in all possible contexts.

#### Example 1
```python
# from views._util.auth

from flask import redirect, url_for
from app.models import Team
import re
```

#### Example 2
```python
from flask import (redirect, render_template, request, session,
	url_for, )

from app.email import sign_in_email
from app.models import Account, Team

import datetime, re
```

<!-- ### View Controllers

### Common Functionality -->
