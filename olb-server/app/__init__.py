from flask_restx import Api
from flask import Blueprint

from .main.controllers.user_controller import api as user_api
from .main.controllers.auth_controller import api as auth_api
from .main.controllers.board_controller import api as board_api
from .main.controllers.submit_controller import api as submit_api
from .main.controllers.notification_controller import api as notification_api

blueprint = Blueprint('api', __name__)
authorizations = {
    "jwt": {
        "type": "apiKey",
        "in": "header",
        "name": "Authorization"
    }
}

api = Api(blueprint,
          title="openLeaderboard",
          version="1.0",
          description="openLeaderboard api",
          authorizations=authorizations
          )

api.add_namespace(auth_api, path="/auth")
api.add_namespace(user_api, path="/user")
api.add_namespace(board_api, path="/board")
api.add_namespace(submit_api, path="/submit")
api.add_namespace(notification_api, path="/notification")
