from flask_restx import Namespace, fields


class NotificationDto:
    namespace = Namespace("notification", description="Notification operations")

    incoming_invite = namespace.model(
        "incoming_invite",
        {
            "from_name": fields.String(required=True, description="sending user's name"),
            "invite_id": fields.Integer(required=True, description="invite's id"),
        },
    )

    outgoing_invite = namespace.model(
        "outgoing_invite",
        {
            "to_name": fields.String(required=True, description="receiving user's name"),
            "invite_id": fields.Integer(required=True, description="invite's id"),
        },
    )

    incoming_submission = namespace.model(
        "incoming_submission",
        {
            "from_name": fields.String(required=True, description="sending user's name"),
            "match_id": fields.Integer(required=True, description="match's id"),
        },
    )

    outgoing_submission = namespace.model(
        "outgoing_submission",
        {
            "to_name": fields.String(required=True, description="receiving user's name"),
            "match_id": fields.Integer(required=True, description="match's id"),
        },
    )

    incoming_invites_response = namespace.model(
        "incoming_invites_response", {"invites": fields.List(fields.Nested(incoming_invite))}
    )

    outgoing_invites_response = namespace.model(
        "outgoing_invites_response", {"invites": fields.List(fields.Nested(outgoing_invite))}
    )

    incoming_submissions_response = namespace.model(
        "incoming_submissions_response", {"matches": fields.List(fields.Nested(incoming_submission))}
    )

    outgoing_submissions_response = namespace.model(
        "outgoing_submissions_response", {"matches": fields.List(fields.Nested(outgoing_submission))}
    )

    invite_response = namespace.model(
        "invite_response",
        {
            "board_id": fields.Integer(required=True, description="Id of the invite's board"),
            "board_name": fields.String(required=True, description="board's name"),
            "public": fields.Boolean(required=True, description="Whether or not this is a public board"),
            "member_count": fields.Integer(required=True, description="Number of board members"),
            "from_id": fields.Integer(required=True, description="Id of the receiving user"),
            "from_name": fields.String(required=True, description="receiving User's username"),
            "to_id": fields.Integer(required=True, description="Id of the sending user"),
            "to_name": fields.String(required=True, description="sending User's username"),
            "invite_id": fields.Integer(required=True, description="the board invite's id"),
        },
    )

    submission_response = namespace.model(
        "invite_response",
        {
            "board_id": fields.Integer(required=True, description="Id of the invite's board"),
            "board_name": fields.String(required=True, description="board's name"),
            "result": fields.String(required=True, description="result of match {'Win', 'Loss', 'Draw'}"),
            "rating change": fields.Float(required=True, description="change to the user's rating from this match"),
            "from_id": fields.Integer(required=True, description="Id of the receiving user"),
            "from_name": fields.String(required=True, description="receiving User's username"),
            "to_id": fields.Integer(required=True, description="Id of the sending user"),
            "to_name": fields.String(required=True, description="sending User's username"),
            "match_id": fields.Integer(required=True, description="the board invite's id"),
        },
    )

    accept_decline_invite = namespace.model(
        "accept_decline_invite",
        {
            "accept": fields.Boolean(
                required=True,
                description="Whether or not the invite is being accepted or declined (or cancelled)\
                                                            {True = accept, False = decline, user is sender = cancel}",
            ),
            "invite_id": fields.Integer(required=True, description="the id of the invite"),
        },
    )

    accept_decline_invite_response = namespace.model(
        "accept_decline_invite_response",
        {
            "success": fields.Boolean(
                required=True, description="Whether or not the invite was successfully accepted/declined/cancelled"
            ),
            "message": fields.String(required=True, description="Description of success or failure"),
        },
    )

    accept_decline_submission = namespace.model(
        "accept_decline_submission",
        {
            "accept": fields.Boolean(
                required=True,
                description="Whether or not the match is being accepted or declined (or cancelled)\
                                                            {True = accept, False = decline, user is sender = cancel}",
            ),
            "match_id": fields.Integer(required=True, description="the id of the match"),
        },
    )

    accept_decline_submission_response = namespace.model(
        "accept_decline_submission_response",
        {
            "success": fields.Boolean(
                required=True, description="Whether or not the invite was successfully accepted/declined/cancelled"
            ),
            "message": fields.String(required=True, description="Description of success or failure"),
        },
    )
