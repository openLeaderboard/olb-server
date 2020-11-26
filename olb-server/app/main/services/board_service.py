from sqlalchemy import and_, or_
from enum import Enum
from flask_jwt_extended import get_jwt_identity

from app.main import db
from app.main.models.db_models.board import Board
from app.main.models.db_models.user_board import UserBoard
from app.main.models.db_models.match import Match
from app.main.models.db_models.user import User
from app.main.models.db_models.board_invite import BoardInvite

from .utils import get_rank_icon


# searches for boards whose name contains the provided string
def search_boards(name):
    boards = (
        db.session.query(
            Board.name.label("name"),
            Board.id.label("id"),
            db.func.count(db.case([(UserBoard.is_active, True)])).label("member_count"),
        )
        .outerjoin(UserBoard)
        .group_by(Board.id)
        .filter(Board.name.contains(name))
    )
    boards_dict = list(map(lambda board: board._asdict(), boards))

    return boards_dict


# gets a list of all boards
def get_all_boards():
    boards = (
        db.session.query(
            Board.name.label("name"),
            Board.id.label("id"),
            db.func.count(db.case([(UserBoard.is_active, True)])).label("member_count"),
        )
        .outerjoin(UserBoard)
        .group_by(Board.id)
        .all()
    )
    boards_dict = list(map(lambda board: board._asdict(), boards))

    return boards_dict


# gets match history for specified board
def get_board_activity(board_id):
    to_user = db.aliased(User)
    from_user = db.aliased(User)
    matches = (
        db.session.query(
            to_user.name.label("submitter_name"),
            from_user.name.label("receiver_name"),
            db.case(
                [
                    (Match.winner_user_id == Match.from_user_id, "Win"),
                    (Match.winner_user_id == None, "Draw"),  # noqa E711 -- SQLAlchemy doesn't support "is None"
                ],
                else_="Loss",
            ).label("submitter_result"),
            db.case(
                [
                    (Match.winner_user_id == Match.to_user_id, "Win"),
                    (Match.winner_user_id == None, "Draw"),  # noqa E711 -- SQLAlchemy doesn't support "is None"
                ],
                else_="Loss",
            ).label("receiver_result"),
        )
        .join(to_user, Match.to_user_id == to_user.id)
        .join(from_user, Match.from_user_id == from_user.id)
        .order_by(Match.id.desc())
        .filter(and_(Match.board_id == board_id, Match.is_verified))
    )

    matches_dict = list(map(lambda match: match._asdict(), matches))

    return matches_dict


# gets all users for the specified board
def get_normal_board_users(board_id):
    return get_board_users(board_id, BoardUserQueryType.NORMAL)


# gets top users for the specified board
def get_top_board_users(board_id):
    return get_board_users(board_id, BoardUserQueryType.TOP)


def get_board_users(board_id, query_type):
    if query_type == BoardUserQueryType.TOP:
        ranked_users_sq = (
            db.session.query(
                UserBoard.board_id,
                UserBoard.user_id,
                UserBoard.rating,
                db.func.rank().over(partition_by=UserBoard.board_id, order_by=UserBoard.rating.desc()).label("rank"),
            )
            .filter(and_(UserBoard.is_active, UserBoard.board_id == board_id))
            .order_by(UserBoard.rating.desc())
            .limit(5)
            .subquery()
        )
    else:
        ranked_users_sq = (
            db.session.query(
                UserBoard.board_id,
                UserBoard.user_id,
                UserBoard.rating,
                db.func.rank().over(partition_by=UserBoard.board_id, order_by=UserBoard.rating.desc()).label("rank"),
            )
            .filter(and_(UserBoard.is_active, UserBoard.board_id == board_id))
            .subquery()
        )

    full_users_query = (
        db.session.query(
            ranked_users_sq.c.user_id,
            User.name.label("name"),
            ranked_users_sq.c.rank,
            ranked_users_sq.c.rating,
            db.func.count()
            .filter(and_(Match.winner_user_id == ranked_users_sq.c.user_id, Match.is_verified))
            .over(partition_by=ranked_users_sq.c.user_id)
            .label("wins"),
            db.func.count()
            .filter(
                and_(
                    Match.winner_user_id != ranked_users_sq.c.user_id,
                    Match.is_verified,
                    or_(ranked_users_sq.c.user_id == Match.from_user_id, ranked_users_sq.c.user_id == Match.to_user_id),
                )
            )
            .over(partition_by=ranked_users_sq.c.user_id)
            .label("losses"),
        )
        .distinct()
        .join(User, User.id == ranked_users_sq.c.user_id)
        .join(Board, ranked_users_sq.c.board_id == Board.id)
        .join(Match, ranked_users_sq.c.board_id == Match.board_id, isouter=True)
        .order_by(ranked_users_sq.c.rank)
        .filter(Board.id == board_id)
    )

    user_count = db.session.query(
        db.func.count().filter(and_(UserBoard.is_active, UserBoard.board_id == board_id))
    ).scalar()

    users_dict = list(map(lambda user: add_icon_convert(user, user_count), full_users_query))

    return users_dict


# gets a board's profile
def get_board_profile(board_id, user_id):
    member_count_sq = db.session.query(
        db.func.count().filter(and_(UserBoard.board_id == board_id, UserBoard.is_active)).label("member_count")
    ).subquery()

    match_count_sq = db.session.query(
        db.func.count().filter(and_(Match.is_verified, Match.board_id == board_id)).label("matches_count")
    ).subquery()

    board_membership_query = (
        db.session.query(
            UserBoard.is_admin,
            UserBoard.is_active,
        )
        .filter(UserBoard.board_id == board_id, UserBoard.user_id == user_id)
        .first()
    )

    profile = (
        db.session.query(
            Board.name.label("board_name"),
            Board.id.label("board_id"),
            Board.is_public,
            member_count_sq.c.member_count,
            match_count_sq.c.matches_count,
        )
        .filter(Board.id == board_id)
        .first()
    )

    board_profile_dict = profile._asdict()
    board_profile_dict["top_members"] = get_top_board_users(board_id)

    if board_membership_query:
        board_profile_dict["is_admin"] = board_membership_query.is_admin
        board_profile_dict["is_member"] = board_membership_query.is_active
    else:
        board_profile_dict["is_admin"] = False
        board_profile_dict["is_member"] = False

    return board_profile_dict


# creates a new board
def create_board(create_board_data):
    creator_id = get_jwt_identity()

    try:
        new_board = Board(name=create_board_data["board_name"], is_public=create_board_data["is_public"])
        db.session.add(new_board)
        db.session.flush()

        new_user_board = UserBoard(
            board_id=new_board.id,
            user_id=creator_id,
            is_admin=True,
        )
        db.session.add(new_user_board)
        db.session.commit()

        response = {
            "success": True,
            "message": "Board successfully created",
            "board_id": new_user_board.board_id,
        }
    except Exception as e:
        print(e)  # TODO error logging
        db.session.rollback()

        response = {
            "success": False,
            "message": "Error creating board",
            "board_id": 0,
        }

    return response


# edits an existing board
def edit_board(edit_board_data):
    user_id = get_jwt_identity()

    user_board = UserBoard.query.filter_by(board_id=edit_board_data["board_id"], user_id=user_id, is_admin=True).first()

    if not user_board:
        return {
            "success": False,
            "message": "You do not have permissions to edit this board",
        }

    try:
        edit_board = Board.query.filter_by(id=user_board.board_id).first()
        edit_board.name = edit_board_data["board_name"]
        edit_board.is_public = edit_board_data["is_public"]
        db.session.add(edit_board)
        db.session.commit()
    except Exception as e:
        print(e)  # TODO logging
        db.session.rollback()

        return {
            "success": False,
            "message": "Error editing board",
        }

    return {
        "success": True,
        "message": "Board successfully updated",
    }


# invite a user to a board (admin only)
def invite_to_board(invite_data):
    inviter_user_id = get_jwt_identity()
    invitee_user_id = invite_data["user_id"]
    board_id = invite_data["board_id"]

    if inviter_user_id == invitee_user_id:
        return {
            "success": False,
            "message": "You cannot invite yourself to a board",
        }

    inviter_user_board = UserBoard.query.filter_by(board_id=board_id, user_id=inviter_user_id, is_admin=True).first()
    if not inviter_user_board:
        return {
            "success": False,
            "message": "You do not have permissions to invite to this board",
        }

    invitee_user_board = UserBoard.query.filter_by(board_id=board_id, user_id=invitee_user_id).first()
    if invitee_user_board and invitee_user_board.is_active:
        return {
            "success": False,
            "message": "User is already a member of this board",
        }

    invite_exists = BoardInvite.query.filter_by(board_id=board_id, to_user_id=invitee_user_id).first()
    if invite_exists:
        return {
            "success": False,
            "message": "User has already been invited to this board",
        }

    try:
        new_invite = BoardInvite(board_id=board_id, to_user_id=invitee_user_id, from_user_id=inviter_user_id)
        db.session.add(new_invite)
        db.session.commit()
    except Exception as e:
        print(e)  # TODO logging
        db.session.rollback()

        return {
            "success": False,
            "message": "Error creating invite",
        }

    return {
        "success": True,
        "message": "User successfully invited",
    }


# join a board
def join_board(join_data):
    user_id = get_jwt_identity()
    board_id = join_data["board_id"]

    public_board = Board.query.filter_by(id=board_id, is_public=True).first()
    if not public_board:
        return {
            "success": False,
            "message": "You do not have permission to join this board",
        }

    user_member = UserBoard.query.filter_by(board_id=board_id, user_id=user_id).first()
    try:
        if user_member:
            if user_member.is_active:
                return {
                    "success": False,
                    "message": "You're already a member of this board",
                }

            user_member.is_active = True
            db.session.add(user_member)
            db.session.commit()
        else:
            new_member = UserBoard(board_id=board_id, user_id=user_id)
            db.session.add(new_member)
            db.session.commit()
    except Exception as e:
        print(e)  # TODO logging
        db.session.rollback()

        return {
            "success": False,
            "message": "Error joining board",
        }

    return {
        "success": True,
        "message": "Successfully joined board",
    }


# leave a board
def leave_board(leave_data):
    user_id = get_jwt_identity()
    board_id = leave_data["board_id"]

    user_board = UserBoard.query.filter_by(board_id=board_id, user_id=user_id).first()
    if user_board:
        if user_board.is_admin:
            return {
                "success": False,
                "message": "You cannot leave a board you created",
            }

        try:
            user_board.is_active = False
            db.session.add(user_board)
            db.session.commit()
        except Exception as e:
            print(e)  # TODO logging
            db.session.rollback()

            return {
                "success": False,
                "message": "Error leaving board",
            }

    return {
        "success": True,
        "message": "Successfully left board",
    }


# remove someone from a board
def remove_from_board(remove_data):
    remover_user_id = get_jwt_identity()
    removee_user_id = remove_data["user_id"]
    board_id = remove_data["board_id"]

    if remover_user_id == removee_user_id:
        return {
            "success": False,
            "message": "You cannot remove yourself from a board",
        }

    remover_user_board = UserBoard.query.filter_by(board_id=board_id, user_id=remover_user_id, is_admin=True).first()
    if not remover_user_board:
        return {
            "success": False,
            "message": "You do not have permissions to remove players from this board",
        }

    removee_user_board = UserBoard.query.filter_by(board_id=board_id, user_id=removee_user_id).first()
    if removee_user_board:
        if removee_user_board.is_admin:
            return {
                "success": False,
                "message": "You cannot remove an admin from a board",
            }

        try:
            removee_user_board.is_active = False
            db.session.add(removee_user_board)
            db.session.commit()
        except Exception as e:
            print(e)  # TODO logging
            db.session.rollback()

            return {
                "success": False,
                "message": "Error removing user from board",
            }

    return {
        "success": True,
        "message": "Successfully removed user from board",
    }


# converts the given query result to a dict and computes its rank icon
def add_icon_convert(board, users_count):
    board_dict = board._asdict()
    board_dict["rank_icon"] = get_rank_icon(board_dict["rank"], users_count).value

    return board_dict


class BoardUserQueryType(Enum):
    NORMAL = 1
    TOP = 2
