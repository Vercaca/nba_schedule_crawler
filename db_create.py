from bot.db import db
from models import User

# create all
db.create_all()

# insert data
db.session.add(User(reply_token="token_1",
                    message="hey"))

# commit the changes
db.session.commit()
