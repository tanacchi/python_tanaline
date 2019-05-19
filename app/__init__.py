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

import os

server = Flask(__name__)

CHANNEL_ACCESS_TOKEN = os.environ['CHANNEL_ACCESS_TOKEN']
CHANNEL_SECRET       = os.environ['CHANNEL_SECRET']
server.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)
db = SQLAlchemy(server)


class Talk(db.Model):
    id      = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(80))
    content = db.Column(db.String(200))

    def __init__(self, user_id, content):
        self.user_id = user_id
        self.content = content


@server.route("/webhook", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    server.logger.info("Request body: " + body)

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
        TextSendMessage(text="Hello, I'm written in Python."))
    if event.type == 'message' and event.message.type == 'text':
        source_type = event.source.type
        talk = Talk(event.source.user_id, event.message.text)
        db.session.add(talk)
        db.session.commit()