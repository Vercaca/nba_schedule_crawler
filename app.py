import os

from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)


__CHANNEL_ACCESS_TOKEN__ = 'mF7WyHTQdEpMQhgFln6+klYO5hrrKngIIg8cl5G8uPHg4b2Rd0tlnH/4ObLk9mSXRMEuZ6ya/FpLx8fkvSgTRooYKwD1rvVQ2oMj1m+fkW52Tno9N1KdWMtWMPaSbi+2bNzTV0SUbP4axaUQyQc0CgdB04t89/1O/w1cDnyilFU='  # YOUR_CHANNEL_ACCESS_TOKEN
__CHANNEL_SECRET__ = 'fc8aa1a7bfe463c80b0f50de599eec94'  # YOUR_CHANNEL_SECRET

app = Flask(__name__)

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
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
