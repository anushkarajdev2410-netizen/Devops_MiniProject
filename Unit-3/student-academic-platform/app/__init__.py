import os
from flask import Flask
from .routes import api
from .db import init_db

def create_app(test_config=None):
    app = Flask(__name__)
    app.config.update(
        DATABASE=os.getenv("DATABASE", "student_platform.db"),
        TESTING=False,
    )
    if test_config:
        app.config.update(test_config)
    init_db(app)
    app.register_blueprint(api, url_prefix="/api")
    return app
