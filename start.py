import os
from app import app as contest_server

if __name__ == "__main__":
    conf = os.getenv("FLASK_CONFIG", "config.default.DevConfig")
    contest_server.create_app(conf).run(host='0.0.0.0')
