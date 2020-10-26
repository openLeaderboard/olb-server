from sqlalchemy.orm import relationship

from app.main import db


# db model for matches (pending and verified)
class Match(db.Model):
    __tablename__ = "match"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    from_user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    to_user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    board_id = db.Column(db.Integer, db.ForeignKey("board.id"), nullable=False)
    winner_user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)
    winner_rating_change = db.Column(db.Float, nullable=False)
    verified = db.Column(db.Boolean, nullable=False, default=False)

    from_user = relationship("User", backref="sent_match", foreign_keys=[from_user_id])
    to_user = relationship("User", backref="received_match", foreign_keys=[to_user_id])
    board = relationship("Board", back_populates="matches")
