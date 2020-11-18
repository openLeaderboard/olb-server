from flask_jwt_extended import get_jwt_identity
from elo import rate_1vs1

from app.main import db
from app.main.models.db_models.match import Match
from app.main.models.db_models.user_board import UserBoard


# submit a match
def submit_match(submit_data):
    result_string = submit_data["result"].lower()
    from_user_id = get_jwt_identity()
    to_user_id = submit_data["user_id"]
    board_id = submit_data["board_id"]

    if result_string == "win":
        winner_user_id = from_user_id
    elif result_string == "loss":
        winner_user_id = to_user_id
    elif result_string == "draw":
        winner_user_id = None
    else:
        return {
            "success": False,
            "message": "Invalid result status",
        }

    if from_user_id == to_user_id:
        return {
            "success": False,
            "message": "You cannot submit a match to yourself",
        }

    from_user_board = UserBoard.query.filter_by(board_id=board_id, user_id=from_user_id, is_active=True).first()
    to_user_board = UserBoard.query.filter_by(board_id=board_id, user_id=to_user_id, is_active=True).first()

    if not (to_user_board and from_user_board):
        return {
            "success": False,
            "message": "Could not submit match - one or both users are not members of the board",
        }

    from_user_rating_change, to_user_rating_change = calculate_elo_change(
        from_user_board, to_user_board, winner_user_id
    )

    try:
        new_match = Match(
            from_user_id=from_user_id,
            to_user_id=to_user_id,
            board_id=board_id,
            winner_user_id=winner_user_id,
            from_user_rating_change=from_user_rating_change,
            to_user_rating_change=to_user_rating_change,
        )

        db.session.add(new_match)
        db.session.commit()
    except Exception as e:
        print(e)  # TODO logging
        db.session.rollback()

        return {
            "success": False,
            "message": "Error submitting match",
        }

    return {
        "success": True,
        "message": "Successfully submitted match",
    }


# calculate change in elo for each player
def calculate_elo_change(from_user_board, to_user_board, winner_id):
    if winner_id is None:
        from_user_end_rating, to_user_end_rating = rate_1vs1(from_user_board.rating, to_user_board.rating, drawn=True)
    elif winner_id == from_user_board.user_id:
        from_user_end_rating, to_user_end_rating = rate_1vs1(from_user_board.rating, to_user_board.rating)
    else:
        to_user_end_rating, from_user_end_rating = rate_1vs1(to_user_board.rating, from_user_board.rating)

    from_user_rating_change = from_user_end_rating - from_user_board.rating
    to_user_rating_change = to_user_end_rating - to_user_board.rating

    return (from_user_rating_change, to_user_rating_change)
