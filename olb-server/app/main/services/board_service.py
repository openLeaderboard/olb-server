from app.main import db
from app.main.models.db_models.board import Board
from app.main.models.db_models.user_board import UserBoard


# searches for boards whose name contains the provided string
def search_boards(name):
    boards = db.session.query(
                Board.name.label("name"),
                Board.id.label("id"),
                db.func.count(db.case([(UserBoard.is_active, True)])).label("member_count")
            ).outerjoin(UserBoard).group_by(Board.id).filter(Board.name.contains(name))
    boards_dict = list(map(lambda board: board._asdict(), boards))

    response = {
        "search_result": boards_dict
    }
    return response


# gets a list of all boards
def get_all_boards():
    boards = db.session.query(
                Board.name.label("name"),
                Board.id.label("id"),
                db.func.count(db.case([(UserBoard.is_active, True)])).label("member_count")
            ).outerjoin(UserBoard).group_by(Board.id).all()
    boards_dict = list(map(lambda board: board._asdict(), boards))

    response = {
        "search_result": boards_dict
    }
    return response
