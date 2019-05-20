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

app = Flask(__name__)

CHANNEL_ACCESS_TOKEN = os.environ['CHANNEL_ACCESS_TOKEN']
CHANNEL_SECRET       = os.environ['CHANNEL_SECRET']
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)
db = SQLAlchemy(app)


class Talk(db.Model):
    id      = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(80))
    content = db.Column(db.String(200))

    def __init__(self, user_id, content):
        self.user_id = user_id
        self.content = content
