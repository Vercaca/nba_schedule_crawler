import os

from flask import Flask, request, abort
from flask_sqlalchemy import SQLAlchemy

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)


__CHANNEL_ACCESS_TOKEN__ = os.environ.get('CHANNEL_ACCESS_TOKEN', None)  # YOUR_CHANNEL_ACCESS_TOKEN
__CHANNEL_SECRET__ = os.environ.get('CHANNEL_SECRET', None)  # YOUR_CHANNEL_SECRET

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', None)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models import add_user
line_bot_api = LineBotApi(__CHANNEL_ACCESS_TOKEN__)
handler = WebhookHandler(__CHANNEL_SECRET__)


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/test')
def test_page():
    return 'In test page!'


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    print(request.authorization)
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)

    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    add_user(event.reply_token, event.message)

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))
    # print(User.query.all())
    reply_msg = f'你剛剛說 {event.message.text}!'
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply_msg))


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
