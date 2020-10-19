from flask_restx import Namespace, fields


class UserDto:
    namespace = Namespace("user", description="User operations")

    register_user = namespace.model("register_user", {
        "email": fields.String(required=True, description="User's email address"),
        "name": fields.String(required=True, description="User's username"),
        "password": fields.String(required=True, description="User's password in plaintext")
    })
