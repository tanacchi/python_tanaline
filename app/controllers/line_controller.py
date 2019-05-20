from app import (
    flask_app, request, abort,
    line_bot_api, handler,
    db
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)
from app.models.talk import Talk
import urllib.request as urlreq


@flask_app.route("/webhook", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    flask_app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    text_messages = [TextSendMessage(text="Hello, I'm written in Python.")]
    if event.type == 'message' and event.message.type == 'text':
        if event.message.text == "履歴":
            talks = db.session.query(Talk).filter_by(user_id=event.source.user_id)
            for talk in talks:
                text_messages.append(TextSendMessage(text=talk.content))
        elif event.message.text == "送信":
            url = "https://tanacchi-birdbrains.herokuapp.com/line"
            req = urlreq.Request(url)
            with urlreq.urlopen(req) as res:
                text_messages.append(TextSendMessage(text=req.read().decode()))
        else:
            talk = Talk(event.source.user_id, event.message.text)
            db.session.add(talk)
            db.session.commit()

        line_bot_api.reply_message(event.reply_token, text_messages[-5:])
