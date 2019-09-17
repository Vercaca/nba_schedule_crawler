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


__LINE_CHANNEL_ACCESS_TOKEN__ = 'Rg7Ts917dOkKpnOqlGTklZrro3dOJ4BOuZro3zAajzp/' \
                                'Z1O+h+dyTpQer6nYfTn1RMEuZ6ya/FpLx8fkvSgTRooY' \
                                'KwD1rvVQ2oMj1m+fkW6gjv1HnxvZn7pFfMovLdPo1AiY' \
                                'h4rI+kQqzUyHS6nlwwdB04t89/1O/w1cDnyilFU='  # YOUR_CHANNEL_ACCESS_TOKEN
__WEBHOOK_CHANNEL_SECRET__ = 'fc8aa1a7bfe463c80b0f50de599eec94'  # YOUR_CHANNEL_SECRET

app = Flask(__name__)

line_bot_api = LineBotApi(__LINE_CHANNEL_ACCESS_TOKEN__)
handler = WebhookHandler(__WEBHOOK_CHANNEL_SECRET__)


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

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
    app.run()