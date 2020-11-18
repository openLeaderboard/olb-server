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
        .filter(and_(Match.id == match_id, ~Match.is_verified, or_(Match.to_user_id == user_id, BoardInvite.from_user_id == user_id)))
        .first()
    )

    if not match:
        return match

    match_dict = match._asdict()

    return match_dict
