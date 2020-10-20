from flask_restx import Api
from flask import Blueprint

from .main.controllers.user_controller import api as user_api
from .main.controllers.auth_controller import api as auth_api

blueprint = Blueprint('api', __name__)
authorizations = {
    "jwt": {
        "type": "apiKey",
        "in": "header",
        "name": "Authorization"
    }
}

api = Api(blueprint,
          title='openLeaderboard',
          version='1.0',
          description='openLeaderboard api',
          authorizations=authorizations
          )

api.add_namespace(user_api, path='/user')
api.add_namespace(auth_api, path='/auth')
