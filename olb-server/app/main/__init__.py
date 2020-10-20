from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

from .config import configs

db = SQLAlchemy()
jwt = JWTManager()


# Creates an app version depending on the config name
def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(configs[config_name])
    db.init_app(app)
    jwt.init_app(app)

    return app
