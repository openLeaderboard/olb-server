from passlib.hash import argon2
from sqlalchemy.orm import relationship

from app.main import db


# User database model
class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    name = db.Column(db.String(50), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    user_boards = relationship("UserBoard", back_populates="user")
    # sent_board_invites = relationship("BoardInvite", back_populates="from_user", foreign_keys="board_invite.from_user_id")
    # received_board_invites = relationship("BoardInvite", back_populates="to_user", foreign_keys="board_invite.to_user_id")

    @property
    def password(self):
        raise AttributeError("Password is a write-only field")

    @password.setter
    def password(self, password):
        self.password_hash = argon2.hash(password)

    def check_password(self, password):
        return argon2.verify(password, self.password_hash)
