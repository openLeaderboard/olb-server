from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from .config import configs

db = SQLAlchemy()


# Creates an app version depending on the config name
def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(configs[config_name])
    db.init_app(app)

    return app
