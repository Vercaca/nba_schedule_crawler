from app import db


class User(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    reply_token = db.Column(db.String, nullable=True)
    message = db.Column(db.String, nullable=True)

    def __repr__(self):
        return f'<reply msg: {self.reply_token},' \
            f'message: {self.message}>'
