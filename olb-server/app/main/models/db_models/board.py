from sqlalchemy.orm import relationship

from app.main import db


# Board database model
class Board(db.Model):
    __tablename__ = "board"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    public = db.Column(db.Boolean, nullable=False, default=True)

    user_boards = relationship("UserBoard", back_populates="board")
    board_invites = relationship("BoardInvites", back_populates="board")
