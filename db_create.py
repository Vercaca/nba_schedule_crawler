from bot.db import db
from models import UserMessage

# create all
db.create_all()

# insert data
db.session.add(UserMessage(id_='test_id', type='text', user_token="token_1",
               text="hey"))

# commit the changes
db.session.commit()
