from bot.db import db
from models import app
from models import UserMessage
# from flask_sqlalchemy import SQLAlchemy
# create all
db.init_app(app)
db.create_all()

# insert data
db.session.add(UserMessage('id', 'user token', 'type', 'text'))

#
# commit the changes
db.session.commit()
