import os
from flask import Flask
from bot.db import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', None)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


class UserMessage(db.Model):

    __tablename__ = "user_messages"

    id = db.Column(db.String, primary_key=True, autoincrement=False)
    user_token = db.Column(db.String, nullable=False)
    type = db.Column(db.String, nullable=False)
    text = db.Column(db.String, nullable=True)

    def __init__(self, id_, user_token, type, text):
        self.id = id_
        self.user_token = user_token
        self.type = type
        self.text = text

    def __repr__(self):
        return f'user_token: {self.user_token},' \
            f'text: {self.text}>'


def add_user(id_, user_token, type_, text):
    db.session.add(UserMessage(id_, user_token, type_, text))
    db.session.commit()
