from sqlalchemy import and_, or_
from flask_jwt_extended import get_jwt_identity

from app.main import db
from app.main.models.db_models.board_invite import BoardInvite
from app.main.models.db_models.user import User
from app.main.models.db_models.match import Match
from app.main.models.db_models.board import Board
from app.main.models.db_models.user_board import UserBoard


# get the specified user's incoming board invites
def get_incoming_invites(user_id):
    invites = (
        db.session.query(
            BoardInvite.id.label("invite_id"),
            User.name.label("from_name"),
        )
        .join(User, BoardInvite.from_user_id == User.id)
        .filter(BoardInvite.to_user_id == user_id)
        .order_by(BoardInvite.id.desc())
    )

    invites_dict = list(map(lambda invite: invite._asdict(), invites))

    return invites_dict


# get the specified user's outgoing board invites
def get_outgoing_invites(user_id):
    invites = (
        db.session.query(
            BoardInvite.id.label("invite_id"),
            User.name.label("to_name"),
        )
        .join(User, BoardInvite.to_user_id == User.id)
        .filter(BoardInvite.from_user_id == user_id)
        .order_by(BoardInvite.id.desc())
    )

    invites_dict = list(map(lambda invite: invite._asdict(), invites))

    return invites_dict


# get the specified user's incoming match submissions
def get_incoming_matches(user_id):
    matches = (
        db.session.query(
            Match.id.label("match_id"),
            User.name.label("from_name"),
        )
        .join(User, Match.from_user_id == User.id)
        .filter(and_(Match.to_user_id == user_id, ~Match.is_verified))
        .order_by(Match.id.desc())
    )

    matches_dict = list(map(lambda match: match._asdict(), matches))

    return matches_dict


# get the specified user's outgoing match submissions
def get_outgoing_matches(user_id):
    matches = (
        db.session.query(
            Match.id.label("match_id"),
            User.name.label("to_name"),
        )
        .join(User, Match.to_user_id == User.id)
        .filter(and_(Match.from_user_id == user_id, ~Match.is_verified))
        .order_by(Match.id.desc())
    )

    matches_dict = list(map(lambda match: match._asdict(), matches))

    return matches_dict


# get the details of an invite
# will return all null fields if the user does not have permission to view the invite
def get_invite(invite_id):
    to_user = db.aliased(User)
    from_user = db.aliased(User)

    user_id = get_jwt_identity()

    member_count_sq = (
        db.session.query(
            db.func.count()
            .filter(and_(UserBoard.board_id == BoardInvite.board_id, UserBoard.is_active))
            .label("member_count")
        )
        .join(BoardInvite, BoardInvite.board_id == UserBoard.board_id)
        .filter(BoardInvite.id == invite_id)
        .subquery()
    )

    invite = (
        db.session.query(
            BoardInvite.id.label("invite_id"),
            BoardInvite.board_id,
            Board.name.label("board_name"),
            Board.is_public,
            to_user.id.label("to_id"),
            to_user.name.label("to_name"),
            from_user.id.label("from_id"),
            from_user.name.label("from_name"),
            member_count_sq.c.member_count,
        )
        .join(to_user, BoardInvite.to_user_id == to_user.id)
        .join(from_user, BoardInvite.from_user_id == from_user.id)
        .join(Board, BoardInvite.board_id == Board.id)
        .filter(
            and_(
                BoardInvite.id == invite_id, or_(BoardInvite.to_user_id == user_id, BoardInvite.from_user_id == user_id)
            )
        )
        .first()
    )

    if not invite:
        return invite

    invite_dict = invite._asdict()

    return invite_dict


# get the details of an invite
# will return all null fields if the user does not have permission to view the invite
def get_match(match_id):
    to_user = db.aliased(User)
    from_user = db.aliased(User)

    user_id = get_jwt_identity()

    match = (
        db.session.query(
            Match.id.label("match_id"),
            Match.board_id,
            Board.name.label("board_name"),
            Board.is_public,
            to_user.id.label("to_id"),
            to_user.name.label("to_name"),
            from_user.id.label("from_id"),
            from_user.name.label("from_name"),
            db.case(
                [
                    (Match.winner_user_id == user_id, "Win"),
                    (Match.winner_user_id == None, "Draw"),  # noqa E711 -- SQLAlchemy doesn't support "is None"
                ],
                else_="Loss",
            ).label("result"),
            db.case(
                [
                    (Match.from_user_id == user_id, Match.from_user_rating_change),
                    (Match.to_user_id == user_id, Match.to_user_rating_change),
                ],
            ).label("rating_change"),
        )
        .join(to_user, Match.to_user_id == to_user.id)
        .join(from_user, Match.from_user_id == from_user.id)
        .join(Board, Match.board_id == Board.id)
        .filter(
            and_(
                Match.id == match_id,
                ~Match.is_verified,
                or_(Match.to_user_id == user_id, BoardInvite.from_user_id == user_id),
            )
        )
        .first()
    )

    if not match:
        return match

    match_dict = match._asdict()

    return match_dict


# accept, decline, or cancel an invite
def accept_decline_invite(invite_data):
    user_id = get_jwt_identity()
    invite_id = invite_data["invite_id"]
    accept = invite_data["accept"]

    invite = (
        db.session.query(BoardInvite)
        .filter(
            BoardInvite.id == invite_id, or_(BoardInvite.from_user_id == user_id, BoardInvite.to_user_id == user_id)
        )
        .first()
    )

    if not invite:
        return {
            "success": False,
            "message": "You do not have permission to interact with this invite",
        }

    try:
        if user_id == invite.from_user_id or not accept:
            db.session.delete(invite)
            db.session.commit()

            return {
                "success": True,
                "message": "Successfully cancelled invite"
                if user_id == invite.from_user_id
                else "Successfully declined invite",
            }

        invitee_user_board = UserBoard.query.filter_by(board_id=invite.board_id, user_id=invite.to_user_id).first()
        if invitee_user_board:
            if invitee_user_board.is_active:
                db.session.delete(invite)
                db.session.commit()

                return {
                    "success": False,
                    "message": "You are already a member of this board",
                }

            invitee_user_board.is_active = True
            db.session.add(invitee_user_board)
        else:
            new_user_board = UserBoard(board_id=invite.board_id, user_id=invite.to_user_id)
            db.session.add(new_user_board)

        db.session.delete(invite)
        db.session.commit()
    except Exception as e:
        print(e)  # TODO logging
        db.session.rollback()

        return {
            "success": False,
            "message": "Error occurred accepting/declining invite",
        }

    return {
        "success": True,
        "message": "Successfully accepted board invite",
    }


# accept, decline, or cancel a match
def accept_decline_match(match_data):
    user_id = get_jwt_identity()
    match_id = match_data["match_id"]
    accept = match_data["accept"]

    match = (
        db.session.query(Match)
        .filter(Match.id == match_id, ~Match.is_verified, or_(Match.from_user_id == user_id, Match.to_user_id == user_id))
        .first()
    )

    if not match:
        return {
            "success": False,
            "message": "You do not have permission to interact with this match submission",
        }

    try:
        if user_id == match.from_user_id or not accept:
            db.session.delete(match)
            db.session.commit()

            return {
                "success": True,
                "message": "Successfully cancelled match submission"
                if user_id == match.from_user_id
                else "Successfully declined match submission",
            }

        to_user_board = UserBoard.query.filter_by(board_id=match.board_id, user_id=match.to_user_id).first()
        from_user_board = UserBoard.query.filter_by(board_id=match.board_id, user_id=match.from_user_id).first()

        if not (to_user_board and from_user_board):
            db.session.delete(match)
            db.session.commit()

            return {
                "success": False,
                "message": "Could not verify match - one or both users are not members of the board",
            }

        to_user_board.rating += match.to_user_rating_change
        from_user_board.rating += match.from_user_rating_change
        match.is_verified = True

        db.session.add(to_user_board)
        db.session.add(from_user_board)
        db.session.add(match)
        db.session.commit()
    except Exception as e:
        print(e)  # TODO logging
        db.session.rollback()

        return {
            "success": False,
            "message": "Error occurred accepting/declining match submission",
        }

    return {
        "success": True,
        "message": "Successfully verified match submission",
    }
