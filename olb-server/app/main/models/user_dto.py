from flask_restx import Namespace, fields


class UserDto:
    namespace = Namespace("user", description="User operations")

    register_user = namespace.model("register_user", {
        "email": fields.String(required=True, description="User's email address"),
        "name": fields.String(required=True, description="User's username"),
        "password": fields.String(required=True, description="User's password in plaintext")
    })

    register_user_response = namespace.model("register_user_response", {
        "success": fields.Boolean(required=True, description="Whether or not the user was successfully created"),
        "message": fields.String(required=True, description="Description of success or failure"),
        "access_token": fields.String(description="JWT access token")
    })
