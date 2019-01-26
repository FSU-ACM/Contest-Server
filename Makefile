setup:
	pip install --user pipenv
	pipenv install

dev:
	pipenv run python start.py

test:
	pipenv run pytest
