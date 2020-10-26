from flask_restx import Namespace, fields


class SubmitDto:
    namespace = Namespace("submit", description="Match submission operations")

    submit_match = namespace.model("submit_match", {
        "board_id": fields.Integer(required=True, description="Id of board being submitted to"),
        "user_id": fields.Integer(required=True, description="Id of user being submitted to"),
        "result": fields.String(required=True, description="result of match {'Win', 'Loss', 'Draw'}")
    })

    submit_match_response = namespace.model("submit_match_response", {
        "success": fields.Boolean(required=True, description="Whether or not the result was successfully submitted"),
        "message": fields.String(required=True, description="Description of success or failure")
    })
