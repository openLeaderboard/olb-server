from sqlalchemy import and_

from app.main import db
from app.main.models.db_models.board_invite import BoardInvite
from app.main.models.db_models.user import User
from app.main.models.db_models.match import Match


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
