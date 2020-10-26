from flask import request
from flask_restx import Resource
from flask_jwt_extended import jwt_required

from ..models.submit_dto import SubmitDto
# from ..services.auth_service import login_user, logout_user

api = SubmitDto.namespace


@api.route("/")
class SubmitMatch(Resource):

    @api.doc("Submit a match to the board", security="jwt")
    @api.expect(SubmitDto.submit_match, validate=True)
    @api.marshal_with(SubmitDto.submit_match_response)
    @jwt_required
    def post(self):
        data = request.json
        stub = {
            "success": True,
            "message": "Successfully submitted match",
        }
        return stub
