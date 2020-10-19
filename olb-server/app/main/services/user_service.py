from app.main import db
from app.main.models.db_models.user import User


# Creates a new user, returns error if email already in use
def create_user(user_data):
    user_exists = User.query.filter_by(email=user_data["email"]).first()

    if not user_exists:
        new_user = User(
            email=user_data["email"],
            name=user_data["username"],
            password=user_data["password"]
        )
        db.session.add(new_user)
        db.session.commit()

        response = {
            "success": True,
            "message": "User successfully registered."
        }
    else:
        response = {
            "success": False,
            "message": "Email already in use."
        }

    return response


# searches for users whose name contains the provided string
def search_users(name):
    users = db.session.query(User.name.label("username"), User.id.label("id")).filter(User.name.contains(name))
    users_dict = map(lambda user: user._asdict(), users)

    return list(users_dict)


# gets a list of all users
def get_all_users():
    users = db.session.query(User.name.label("username"), User.id.label("id")).all()
    users_dict = map(lambda user: user._asdict(), users)

    return list(users_dict)
