from sqlalchemy.orm import relationship

from app.main import db


# Connecting table for M:N user:board relationship
class UserBoard(db.Model):
    __tablename__ = "user_board"

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), primary_key=True)
    board_id = db.Column(db.Integer, db.ForeignKey("board.id"), primary_key=True)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    is_favourite = db.Column(db.Boolean, nullable=False, default=False)
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    rating = db.Column(db.Float, nullable=False, default=1200)

    user = relationship("User", back_populates="user_boards")
    board = relationship("Board", back_populates="user_boards")
