from sqlalchemy.orm import relationship

from app.main import db


# db model for leaderboard invites
class BoardInvite(db.Model):
    __tablename__ = "board_invite"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    from_user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    to_user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    board_id = db.Column(db.Integer, db.ForeignKey("board.id"), nullable=False)

    from_user = relationship("User", backref="sent_board_invites", foreign_keys=[from_user_id])
    to_user = relationship("User", backref="received_board_invites", foreign_keys=[to_user_id])
    board = relationship("Board", back_populates="board_invites")
