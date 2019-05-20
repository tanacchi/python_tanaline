from app import (
    flask_app, request, abort,
    line_bot_api, handler,
    InvalidSignatureError,
    MessageEvent, TextMessage, TextSendMessage,
    db
)
from app.models.talk import Talk

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
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text="Hello, I'm written in Python."))
    if event.type == 'message' and event.message.type == 'text':
        source_type = event.source.type
        talk = Talk(event.source.user_id, event.message.text)
        db.session.add(talk)
        db.session.commit()

