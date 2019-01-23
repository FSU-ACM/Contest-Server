import pytest
from app import app as flask_app

@pytest.fixture
def app():
    flask_app.config.from_object('config.default.TestConfig')
    return flask_app
