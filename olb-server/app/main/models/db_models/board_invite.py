from sqlalchemy.orm import relationship

from app.main import db


# db model for leaderboard invites
class BoardInvite(db.Model):
    __tablename__ = "board_invite"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    from_user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    to_user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    board_id = db.Column(db.Integer, db.ForeignKey("board.id"))

    from_user = relationship("User", back_populates="sent_board_invites")
    to_user = relationship("User", back_populates="received_board_invites")
    board = relationship("Board", back_populates="board_invites")
