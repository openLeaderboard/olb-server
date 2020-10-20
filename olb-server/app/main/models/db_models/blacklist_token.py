from app.main import db


# blacklisted jwt
class BlacklistToken(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    jti = db.Column(db.String(120))

    @classmethod
    def is_jti_blacklisted(token, jti):
        is_blacklisted = bool(token.query.filter_by(jti=jti).first())

        return is_blacklisted
