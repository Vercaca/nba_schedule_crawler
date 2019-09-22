import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', None)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class User(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    reply_token = db.Column(db.String, nullable=False)
    message = db.Column(db.String, nullable=True)

    def __repr__(self):
        return f'<reply msg: {self.reply_token},' \
            f'message: {self.message}>'


def add_user(reply_token, message):
    db.session.add(User(reply_token, message))
    db.session.commit()

