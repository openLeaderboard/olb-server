from flask_jwt_extended import create_access_token

from app.main import db
from app.main.models.db_models.blacklist_token import BlacklistToken
from app.main.models.db_models.user import User


def is_token_in_blacklist(decrypted_token):
    jti = decrypted_token["jti"]
    return BlacklistToken.is_jti_blacklisted(jti)


def login_user(login_data):
    user = User.query.filter_by(email=login_data["email"]).first()
    if user and user.check_password(login_data["password"]):
        jwt = create_access_token(identity=user.id)
        response = {
            "success": True,
            "message": "User successfully logged in.",
            "access_token": f"Bearer {jwt}",
        }
    else:
        response = {
            "success": False,
            "message": "Email or password does not match.",
        }

    return response


def logout_user(jti):
    try:
        new_blacklisted_token = BlacklistToken(jti=jti)
        db.session.add(new_blacklisted_token)
        db.session.commit()

        response = {
            "success": True,
            "message": "Access token has been revoked",
        }
    except Exception as e:
        print(e)  # add logging

        response = {
            "success": False,
            "message": "Something went wrong",
        }

    return response
