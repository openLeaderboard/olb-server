from flask import request
from flask_restx import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from ..models.notification_dto import NotificationDto
from ..services.notification_service import (
    get_incoming_invites,
    get_outgoing_invites,
    get_incoming_matches,
    get_outgoing_matches,
    get_invite,
    get_match,
    accept_decline_invite,
    accept_decline_match,
)

api = NotificationDto.namespace


@api.route("/incoming/invites")
class GetIncomingBoardInvites(Resource):
    @api.doc("Get board invites sent to the user", security="jwt")
    @api.marshal_with(NotificationDto.incoming_invites_response)
    @jwt_required
    def get(self):
        user_id = get_jwt_identity()
        response = {
            "invites": get_incoming_invites(user_id),
        }
        return response


@api.route("/incoming/submissions")
class GetIncomingSubmissions(Resource):
    @api.doc("Get match submissions sent to the user", security="jwt")
    @api.marshal_with(NotificationDto.incoming_submissions_response)
    @jwt_required
    def get(self):
        user_id = get_jwt_identity()
        response = {
            "matches": get_incoming_matches(user_id),
        }
        return response


@api.route("/invite")
class AcceptDeclineCancelBoardInvite(Resource):
    @api.doc("Add, Decline, or Cancel a board invite", security="jwt")
    @api.expect(NotificationDto.accept_decline_invite, validate=True)
    @api.marshal_with(NotificationDto.accept_decline_invite_response)
    @jwt_required
    def post(self):
        invite_data = request.json
        return accept_decline_invite(invite_data)


@api.route("/invite/<invite_id>")
@api.param("invite_id", "The specified board invite's id")
class GetBoardInvite(Resource):
    @api.doc("view a specific board invite", security="jwt")
    @api.marshal_with(NotificationDto.invite_response)
    @jwt_required
    def get(self, invite_id):
        return get_invite(invite_id)


@api.route("/outgoing/invites")
class GetOutgoingBoardInvites(Resource):
    @api.doc("Get board invites sent by the user", security="jwt")
    @api.marshal_with(NotificationDto.outgoing_invites_response)
    @jwt_required
    def get(self):
        user_id = get_jwt_identity()
        response = {
            "invites": get_outgoing_invites(user_id),
        }
        return response


@api.route("/outgoing/submissions")
class GetOutgoingSubmissions(Resource):
    @api.doc("Get match submissions sent by the user", security="jwt")
    @api.marshal_with(NotificationDto.outgoing_submissions_response)
    @jwt_required
    def get(self):
        user_id = get_jwt_identity()
        response = {
            "matches": get_outgoing_matches(user_id),
        }
        return response


@api.route("/submission")
class AcceptDeclineCancelSubmission(Resource):
    @api.doc("Add, Decline, or Cancel a match submission", security="jwt")
    @api.expect(NotificationDto.accept_decline_submission, validate=True)
    @api.marshal_with(NotificationDto.accept_decline_submission_response)
    @jwt_required
    def post(self):
        match_data = request.json
        return accept_decline_match(match_data)


@api.route("/submission/<match_id>")
@api.param("match_id", "The specified match's id")
class GetSubmission(Resource):
    @api.doc("view a specific match submission", security="jwt")
    @api.marshal_with(NotificationDto.submission_response)
    @jwt_required
    def get(self, match_id):
        return get_match(match_id)
