from flask import request
from flask_restx import Resource
from flask_jwt_extended import jwt_required

from ..models.submit_dto import SubmitDto
from ..services.submit_service import submit_match

api = SubmitDto.namespace


@api.route("/")
class SubmitMatch(Resource):
    @api.doc("Submit a match to the board", security="jwt")
    @api.expect(SubmitDto.submit_match, validate=True)
    @api.marshal_with(SubmitDto.submit_match_response)
    @jwt_required
    def post(self):
        submit_data = request.json
        return submit_match(submit_data)
