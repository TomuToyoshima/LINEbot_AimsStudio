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
from tenki import withOpenAI

app = Flask(__name__)
line_bot_api = LineBotApi(
    'En1Q2i4+2InzJQKO1wJ+YIxIKoFOKC8VqcLvSkJjckuSmrj0dHrzh79c52OQCDKGJTXbDlgr0S7giPyej6fzCL2yFl+S1Eo8V5R//kM1fItLX4rGXUbvtusMlMNkGWy61mi9msxfkOT3JC020tH7gwdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('25d4b2851f882ea9619257e0e8dd7abf')


@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=withOpenAI(event.message.text)))


if __name__ == "__main__":
    app.run()
