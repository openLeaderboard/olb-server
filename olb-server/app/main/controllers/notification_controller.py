from flask import request
from flask_restx import Resource
from flask_jwt_extended import jwt_required

from ..models.notification_dto import NotificationDto
# from ..services.notification_service import create_user, search_users, get_all_users

api = NotificationDto.namespace


@api.route("/incoming/invites")
class GetIncomingBoardInvites(Resource):

    @api.doc("Get board invites sent to the user", security="jwt")
    @api.marshal_with(NotificationDto.incoming_invites_response)
    @jwt_required
    def get(self):
        stub = {
            "invites": [
                {
                    "from_name": "Paul Dan",
                    "invite_id": 1
                },
                {
                    "from_name": "Parker",
                    "invite_id": 2
                }
            ]
        }
        return stub


@api.route("/incoming/submissions")
class GetIncomingSubmissions(Resource):

    @api.doc("Get match submissions sent to the user", security="jwt")
    @api.marshal_with(NotificationDto.incoming_submissions_response)
    @jwt_required
    def get(self):
        stub = {
            "matches": [
                {
                    "from_name": "Paul Dan",
                    "match_id": 1
                },
                {
                    "from_name": "Parker",
                    "match_id": 2
                }
            ]
        }
        return stub


@api.route("/invite/<invite_id>")
@api.param("invite_id", "The specified board invite's id")
class GetBoardInvite(Resource):

    @api.doc("view a specific board invite", security="jwt")
    @api.marshal_with(NotificationDto.invite_response)
    @jwt_required
    def get(self, invite_id):
        stub = {
            "board_name": "Slap City",
            "board_id": 1,
            "member_count": 10,
            "public": False,
            "from_name": "Paul Dan",
            "from_id": 4,
            "to_name": "Joel",
            "to_id": 1,
            "invite_id": 1
        }
        return stub


@api.route("/outgoing/invites")
class GetOutgoingBoardInvites(Resource):

    @api.doc("Get board invites sent by the user", security="jwt")
    @api.marshal_with(NotificationDto.outgoing_invites_response)
    @jwt_required
    def get(self):
        stub = {
            "invites": [
                {
                    "to_name": "Paul Dan",
                    "invite_id": 3
                },
                {
                    "to_name": "Parker",
                    "invite_id": 4
                }
            ]
        }
        return stub


@api.route("/outgoing/submissions")
class GetOutgoingSubmissions(Resource):

    @api.doc("Get match submissions sent by the user", security="jwt")
    @api.marshal_with(NotificationDto.outgoing_submissions_response)
    @jwt_required
    def get(self):
        stub = {
            "matches": [
                {
                    "to_name": "Paul Dan",
                    "match_id": 3
                },
                {
                    "to_name": "Parker",
                    "match_id": 4
                }
            ]
        }
        return stub


@api.route("/submission/<match_id>")
@api.param("match_id", "The specified match's id")
class GetSubmission(Resource):

    @api.doc("view a specific match submission", security="jwt")
    @api.marshal_with(NotificationDto.submission_response)
    @jwt_required
    def get(self, match_id):
        stub = {
            "board_name": "Slap City",
            "board_id": 1,
            "result": "Win",
            "rating_change": 12.2,
            "from_name": "Paul Dan",
            "from_id": 4,
            "to_name": "Joel",
            "to_id": 1,
            "match_id": 1
        }
        return stub
