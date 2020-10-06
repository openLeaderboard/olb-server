from passlib.hash import argon2

from .. import db


# User database model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    name = db.Column(db.String(50), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    @property
    def password(self):
        raise AttributeError("Password is a write-only field")

    @password.setter
    def password(self, password):
        self.password_hash = argon2.hash(password)

    def check_password(self, password):
        return argon2.verify(password, self.password_hash)
