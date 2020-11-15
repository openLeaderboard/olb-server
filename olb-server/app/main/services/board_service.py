from sqlalchemy import and_

from app.main import db
from app.main.models.db_models.board import Board
from app.main.models.db_models.user_board import UserBoard

from app.main.models.db_models.match import Match
from app.main.models.db_models.user import User


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
