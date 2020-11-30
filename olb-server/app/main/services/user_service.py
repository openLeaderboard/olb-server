from flask_jwt_extended import create_access_token
from enum import Enum
from sqlalchemy import and_, or_, desc, not_
from validate_email import validate_email

from app.main import db
from app.main.models.db_models.user import User
from app.main.models.db_models.board import Board
from app.main.models.db_models.user_board import UserBoard
from app.main.models.db_models.match import Match

from .utils import get_rank_icon


# Creates a new user, returns error if email already in use
def create_user(user_data):
    if not validate_email(user_data["email"]):
        return {
            "success": False,
            "message": "Invalid email",
        }

    user_exists = User.query.filter_by(email=user_data["email"]).first()
    if not user_exists:
        new_user = User(
            email=user_data["email"],
            name=user_data["name"],
            password=user_data["password"],
        )
        db.session.add(new_user)
        db.session.commit()

        jwt = create_access_token(identity=new_user.id)
        response = {
            "success": True,
            "message": "User successfully registered.",
            "access_token": f"Bearer {jwt}",
            "user_id": new_user.id,
        }
    else:
        response = {
            "success": False,
            "message": "Email already in use.",
        }

    return response


# searches for users whose name contains the provided string
def search_users(name):
    users = (
        db.session.query(
            User.name.label("name"),
            User.id.label("id"),
            db.func.count().filter(UserBoard.is_active).label("board_count"),
        )
        .outerjoin(UserBoard)
        .group_by(User.id)
        .order_by(desc("board_count"))
        .filter(User.name.contains(name))
    )

    users_dict = list(map(lambda user: user._asdict(), users))

    return users_dict


# gets a list of all users
def get_all_users():
    users = (
        db.session.query(
            User.name.label("name"),
            User.id.label("id"),
            db.func.count().filter(UserBoard.is_active).label("board_count"),
        )
        .outerjoin(UserBoard)
        .group_by(User.id)
        .order_by(desc("board_count"))
        .all()
    )

    users_dict = list(map(lambda user: user._asdict(), users))

    return users_dict


# gets a list of all users not in the specified board id
def get_all_users_not_in_board(board_id):
    in_board_sq = (
        db.session.query(
            UserBoard.user_id.label("id")
        )
        .filter(UserBoard.board_id == board_id, UserBoard.is_active)
        .subquery()
    )

    users = (
        db.session.query(
            User.name.label("name"),
            User.id.label("id"),
            db.func.count().filter(UserBoard.is_active).label("board_count"),
        )
        .outerjoin(UserBoard)
        .group_by(User.id)
        .order_by(desc("board_count"))
        .filter(not_(User.id.in_(in_board_sq)))
    )

    users_dict = list(map(lambda user: user._asdict(), users))

    return users_dict


# gets a list of all users not in the specified board id
def search_users_not_in_board(name, board_id):
    in_board_sq = (
        db.session.query(
            UserBoard.user_id.label("id")
        )
        .filter(UserBoard.board_id == board_id, UserBoard.is_active)
        .subquery()
    )

    users = (
        db.session.query(
            User.name.label("name"),
            User.id.label("id"),
            db.func.count().filter(UserBoard.is_active).label("board_count"),
        )
        .outerjoin(UserBoard)
        .group_by(User.id)
        .order_by(desc("board_count"))
        .filter(not_(User.id.in_(in_board_sq)))
        .filter(User.name.contains(name))
    )

    users_dict = list(map(lambda user: user._asdict(), users))

    return users_dict


# gets a user's match history
def get_user_activity(user_id):
    matches = (
        db.session.query(
            Board.name.label("board_name"),
            User.name.label("opponent_name"),
            db.case(
                [
                    (Match.winner_user_id == user_id, "Win"),
                    (Match.winner_user_id == None, "Draw"),  # noqa E711 -- SQLAlchemy doesn't support "is None"
                ],
                else_="Loss",
            ).label("result"),
            db.case(
                [(Match.from_user_id == user_id, Match.from_user_rating_change)],
                else_=Match.to_user_rating_change,
            ).label("rating_change"),
        )
        .join(
            User,
            User.id
            == db.case(
                [(Match.from_user_id == user_id, Match.to_user_id)],
                else_=Match.from_user_id,
            ),
        )
        .join(Board)
        .filter(
            and_(
                or_(Match.from_user_id == user_id, Match.to_user_id == user_id),
                Match.is_verified,
            )
        )
        .order_by(Match.id.desc())
    )

    matches_dict = list(map(lambda match: match._asdict(), matches))

    return matches_dict


# gets a user's profile
def get_user_profile(user_id):
    board_count_sq = db.session.query(
        db.func.count().filter(and_(UserBoard.user_id == user_id, UserBoard.is_active)).label("board_count")
    ).subquery()

    match_count_sq = db.session.query(
        db.func.count()
        .filter(
            and_(
                Match.is_verified,
                or_(Match.from_user_id == user_id, Match.to_user_id == user_id),
            )
        )
        .label("matches_count")
    ).subquery()

    profile = (
        db.session.query(
            User.name.label("name"),
            User.id.label("user_id"),
            board_count_sq.c.board_count,
            match_count_sq.c.matches_count,
        )
        .filter(User.id == user_id)
        .first()
    )

    profile_dict = profile._asdict()
    profile_dict["favourite_boards"] = get_favourite_user_boards(user_id)

    return profile_dict


# gets a list of all boards in the user profile format
def get_user_boards(user_id, query_type):
    if query_type is UserBoardQueryType.ADMIN:
        users_boards_sq = (
            db.session.query(UserBoard.board_id)
            .filter(
                and_(
                    UserBoard.user_id == user_id,
                    UserBoard.is_active,
                    UserBoard.is_admin,
                )
            )
            .subquery()
        )
    elif query_type is UserBoardQueryType.FAVOURITE:
        # temporarily just grabbing top 5 boards by rating
        users_boards_sq = (
            db.session.query(UserBoard.board_id)
            .order_by(UserBoard.rating.desc())
            .filter(and_(UserBoard.user_id == user_id, UserBoard.is_active))
            .limit(5)
            .subquery()
        )
    else:
        users_boards_sq = (
            db.session.query(UserBoard.board_id)
            .filter(and_(UserBoard.user_id == user_id, UserBoard.is_active))
            .subquery()
        )

    ranked_boards_sq = (
        db.session.query(
            UserBoard.board_id,
            UserBoard.user_id,
            UserBoard.rating,
            db.func.rank().over(partition_by=UserBoard.board_id, order_by=UserBoard.rating.desc()).label("rank"),
            db.func.count()
            .over(
                partition_by=UserBoard.board_id,
            )
            .label("users_count"),
        )
        .filter(UserBoard.board_id.in_(users_boards_sq))
        .subquery()
    )

    full_boards_query = (
        db.session.query(
            ranked_boards_sq.c.board_id,
            Board.name.label("board_name"),
            ranked_boards_sq.c.rank,
            ranked_boards_sq.c.rating,
            ranked_boards_sq.c.users_count,
            db.func.count()
            .filter(and_(Match.winner_user_id == user_id, Match.is_verified))
            .over(partition_by=ranked_boards_sq.c.board_id)
            .label("wins"),
            db.func.count()
            .filter(and_(Match.winner_user_id != user_id, Match.is_verified))
            .over(partition_by=ranked_boards_sq.c.board_id)
            .label("losses"),
        )
        .distinct()
        .join(Board, ranked_boards_sq.c.board_id == Board.id)
        .join(Match, ranked_boards_sq.c.board_id == Match.board_id, isouter=True)
        .order_by(ranked_boards_sq.c.rating.desc())
        .filter(
            and_(
                ranked_boards_sq.c.user_id == user_id,
                or_(
                    ranked_boards_sq.c.user_id == Match.from_user_id,
                    ranked_boards_sq.c.user_id == Match.to_user_id,
                    Match.id == None,  # noqa E711 -- SQLAlchemy doesn't support "is None"
                ),
            )
        )
    )

    boards_dict = list(map(add_icon_convert, full_boards_query))

    return boards_dict


# get all boards the user is a member of
def get_normal_user_boards(user_id):
    return get_user_boards(user_id, UserBoardQueryType.NORMAL)


# get all boards the user created
def get_admin_user_boards(user_id):
    return get_user_boards(user_id, UserBoardQueryType.ADMIN)


# get all boards the user favourited
# currently just returns top 5 by rating
def get_favourite_user_boards(user_id):
    return get_user_boards(user_id, UserBoardQueryType.FAVOURITE)


# converts the given query result to a dict and computes its rank icon
# no multiline lambdas in python reeeeee
def add_icon_convert(board):
    board_dict = board._asdict()
    board_dict["rank_icon"] = get_rank_icon(board_dict["rank"], board_dict["users_count"]).value

    return board_dict


class UserBoardQueryType(Enum):
    NORMAL = 1
    ADMIN = 2
    FAVOURITE = 3
    NOT_FAVOURITE = 4
