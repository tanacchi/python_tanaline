from flask import Flask, request, abort
from flask_sqlalchemy import SQLAlchemy

from linebot import (
    LineBotApi, WebhookHandler
)
import os

flask_app = Flask(__name__)

CHANNEL_ACCESS_TOKEN = os.environ['CHANNEL_ACCESS_TOKEN']
CHANNEL_SECRET       = os.environ['CHANNEL_SECRET']
flask_app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)
db = SQLAlchemy(flask_app)
