from flask_jwt_extended import create_access_token

from app.main import db
from app.main.models.db_models.user import User
from app.main.models.db_models.user_board import UserBoard


# Creates a new user, returns error if email already in use
def create_user(user_data):
    user_exists = User.query.filter_by(email=user_data["email"]).first()

    if not user_exists:
        new_user = User(
            email=user_data["email"],
            name=user_data["name"],
            password=user_data["password"]
        )
        db.session.add(new_user)
        db.session.commit()

        jwt = create_access_token(identity=new_user.id)
        response = {
            "success": True,
            "message": "User successfully registered.",
            "access_token": f"Bearer {jwt}"
        }
    else:
        response = {
            "success": False,
            "message": "Email already in use."
        }

    return response


# searches for users whose name contains the provided string
def search_users(name):
    users = db.session.query(
                User.name.label("name"),
                User.id.label("id"),
                db.func.count(db.case([(UserBoard.is_active, True)])).label("board_count")
            ).outerjoin(UserBoard).group_by(User.id).filter(User.name.contains(name))
    users_dict = list(map(lambda user: user._asdict(), users))

    response = {
        "search_result": users_dict
    }
    return response


# gets a list of all users
def get_all_users():
    users = db.session.query(
                User.name.label("name"),
                User.id.label("id"),
                db.func.count(db.case([(UserBoard.is_active, True)])).label("board_count")
            ).outerjoin(UserBoard).group_by(User.id).all()
    users_dict = list(map(lambda user: user._asdict(), users))

    response = {
        "search_result": users_dict
    }
    return response
