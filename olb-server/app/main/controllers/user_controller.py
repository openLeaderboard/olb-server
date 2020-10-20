from flask import request
from flask_restx import Resource
from flask_jwt_extended import jwt_required

from ..models.user_dto import UserDto
from ..services.user_service import create_user, search_users, get_all_users

api = UserDto.namespace


@api.route("/register")
class RegisterUser(Resource):

    @api.doc("Create a new user")
    @api.expect(UserDto.register_user, validate=True)
    @api.marshal_with(UserDto.register_user_response)
    def post(self):
        user_data = request.json
        return create_user(user_data=user_data)


@api.route("/search")
class GetAllUsers(Resource):

    @api.doc("Get all users, token required", security="jwt")
    @jwt_required
    def get(self):
        return get_all_users()


@api.route("/search/<username>")
@api.param("username", "The username being searched")
class SearchUsers(Resource):

    @api.doc("Search for users containing <username> string, token required", security="jwt")
    @jwt_required
    def get(self, username):
        return search_users(username)
