from flask import request
from flask_restx import Resource
from flask_jwt_extended import jwt_required, get_raw_jwt

from ..models.auth_dto import AuthDto
from ..services.auth_service import login_user, logout_user

api = AuthDto.namespace


@api.route("/login")
class LoginUser(Resource):

    @api.doc("Log the user in")
    @api.expect(AuthDto.login_user, validate=True)
    @api.marshal_with(AuthDto.login_user_response)
    def post(self):
        login_data = request.json
        return login_user(login_data=login_data)


@api.route("/logout")
class LogoutUser(Resource):

    @api.doc("Log the user out", security="jwt")
    @api.marshal_with(AuthDto.logout_user_response)
    @jwt_required
    def get(self):
        jti = get_raw_jwt()["jti"]
        return logout_user(jti=jti)
