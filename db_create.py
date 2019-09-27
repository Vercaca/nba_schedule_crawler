from bot.db import db
<<<<<<< HEAD
from models import UserMessage
=======
from models import User
>>>>>>> 24b525a9d92a3df61948491bcfcf6d6e87bf2c31

# create all
db.create_all()

# insert data
db.session.add(UserMessage(id_='test_id', type='text', user_token="token_1",
               text="hey"))

# commit the changes
db.session.commit()
