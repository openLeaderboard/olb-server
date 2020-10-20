from flask_restx import Namespace, fields


class AuthDto:
    namespace = Namespace("auth", description="Authentication operations")

    login_user = namespace.model("auth_details", {
        "email": fields.String(required=True, description="User's email address"),
        "password": fields.String(required=True, description="User's password")
    })

    login_user_response = namespace.model("login_user_response", {
        "success": fields.Boolean(required=True, description="Whether or not the user was successfully logged in"),
        "message": fields.String(required=True, description="Description of success or failure"),
        "access_token": fields.String(description="JWT access token")
    })

    logout_user_response = namespace.model("logout_user_response", {
        "success": fields.Boolean(required=True, description="Whether or not the user's token was successfully blacklisted"),
        "message": fields.String(required=True, description="Description of success or failure")
    })
