import os
from datetime import datetime
from db_operator.read_from_db import check_warn, read_town_code
from flask import Flask, abort, request, render_template

# https://github.com/line/line-bot-sdk-python
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
# 更新 LocationMessage
from linebot.models import MessageEvent, TextMessage, TextSendMessage, LocationMessage
from linebot_reply import input_text, input_location

app = Flask(__name__)

line_bot_api = LineBotApi(os.environ.get("CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.environ.get("CHANNEL_SECRET"))


@app.route("/", methods=["GET", "POST"])
def callback():

    if request.method == "GET":
        return render_template("index.html")
    if request.method == "POST":
        signature = request.headers["X-Line-Signature"]
        body = request.get_data(as_text=True)

        try:
            handler.handle(body, signature)
        except InvalidSignatureError:
            abort(400)

        return "OK"


# search route
@ app.route('/search', methods=['GET'])
def search_get():
    return render_template("search.html")


@handler.add(MessageEvent, message=TextMessage)  # 根據行政區判斷Warning
def handle_message_text(event):
    get_message = event.message.text
    # Send To Line
    line_bot_api.reply_message(event.reply_token, input_text(get_message))


@handler.add(MessageEvent, message=LocationMessage)  # 根據行政區和經緯度判斷warning
def handle_message_location(event):
    get_message = event.message.address
    latitude = event.message.latitude
    longitude = event.message.longitude
    # Send To Line
    line_bot_api.reply_message(event.reply_token, input_location(get_message, latitude, longitude))
