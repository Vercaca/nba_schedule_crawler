import os
from flask_sqlalchemy import SQLAlchemy
from flask import Flask

from bot.db import db
# from models import app
from models import UserMessage
# from flask_sqlalchemy import SQLAlchemy
# create all

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', None)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
db.create_all()

# insert data
db.session.add(UserMessage(id_='test_id', type='text', user_token="token_1",
               text="hey"))

#
# commit the changes
db.session.commit()
