import pytest
from flask import url_for

class TestApp:

    def test_config(self, app):
        assert app.config['TEAM_COUNT'] == 5
