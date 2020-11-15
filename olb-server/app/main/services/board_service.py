from sqlalchemy import and_, or_
from enum import Enum

from app.main import db
from app.main.models.db_models.board import Board
from app.main.models.db_models.user_board import UserBoard

from app.main.models.db_models.match import Match
from app.main.models.db_models.user import User

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
def get_board_profile(board_id):
    member_count_sq = db.session.query(
        db.func.count().filter(and_(UserBoard.board_id == board_id, UserBoard.is_active)).label("member_count")
    ).subquery()

    match_count_sq = db.session.query(
        db.func.count().filter(and_(Match.is_verified, Match.board_id == board_id)).label("matches_count")
    ).subquery()

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

    return board_profile_dict


# converts the given query result to a dict and computes its rank icon
def add_icon_convert(board, users_count):
    board_dict = board._asdict()
    board_dict["rank_icon"] = get_rank_icon(board_dict["rank"], users_count).value

    return board_dict


class BoardUserQueryType(Enum):
    NORMAL = 1
    TOP = 2
