from flask_restx import Api
from flask import Blueprint

from .main.controllers.user_controller import api as user_api

blueprint = Blueprint('api', __name__)

api = Api(blueprint,
          title='openLeaderboard',
          version='1.0',
          description='openLeaderboard api'
          )

api.add_namespace(user_api, path='/user')
