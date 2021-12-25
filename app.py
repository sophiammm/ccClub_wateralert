import os
from flask import Flask, abort, request, render_template, jsonify, g
from wtforms import SelectField
from flask_wtf import FlaskForm
from db_operator.read_from_db import read_city, read_town_by_city_code, read_address_by_town_code
from db_operator.update import update_user_location
from judgement.initial_check import message_text, message_location
from gps_address import gps_to_address
from auth import bp
from reply import input_text


# https://github.com/line/line-bot-sdk-python
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
# 更新 LocationMessage
from linebot.models import MessageEvent, TextMessage, TextSendMessage, LocationMessage
from reply import input_text, input_location


# set configuration values
class Config:
    SCHEDULER_API_ENABLED = True
    SCHEDULER_TIMEZONE = "Asia/Taipei"  # <========== 設置時區, 時區不一致可能會導致任務時間出錯
    SECRET_KEY = os.getenv("CSRF_KEY")


# init server
def create_app():
    app = Flask(__name__)
    with app.app_context():
        app.config.from_object(Config())
        # 測試階段先開啟DEBUG, 正式運行要關掉
        app.config['DEBUG'] = True
    return app


app = create_app()


# 定義表格
class AddressForm(FlaskForm):
    city = SelectField("city", choices=[])
    town = SelectField("town", choices=[])


# for linebot
line_bot_api = LineBotApi(os.environ.get("CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.environ.get("CHANNEL_SECRET"))


# route
@app.route("/", methods=["GET", "POST"])
def index():

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


# auth route
app.register_blueprint(bp)


# search route
@ app.route("/location", methods=["GET", "POST"])
def locate():
    if request.method == "GET":
        return render_template("location.html")
    if request.method == "POST":
        data = request.get_json()
        if data == "":
            print("No data")
        else:
            print(data)
            lat = data["lat"]
            lon = data["lon"]
            mark = (lat, lon)
            address = gps_to_address(mark)
            if g.user != None:
                update_user_location(g.user["id"], lat, lon)
        return jsonify({"address": address})


@ app.route("/address")
def select():
    form = AddressForm()
    form.city.choices = read_city()
    return render_template("address.html", form=form)


@ app.route("/select/town/<city_code>")
def town_by_city(city_code):
    towns = read_town_by_city_code(city_code)
    return jsonify({"town_city": towns})


@ app.route("/result", methods=['POST'])
def search_request():
    if request.method == 'POST':
        town_code = request.values["town"]
        address = "".join(read_address_by_town_code(town_code)[0])
        msg = input_text(town_code)
        water_msgs = msg["water"].split("\n")
        rain_msgs = msg["rain"].split("\n")
        reservoir_msgs = msg["reservoir"].split("\n")
        return render_template("result.html", address=address, water_msgs=water_msgs, rain_msgs=rain_msgs, reservoir_msgs=reservoir_msgs)


@handler.add(MessageEvent, message=TextMessage)  # 根據行政區判斷Warning
def handle_message_text(event):
    get_message = event.message.text
    # get user_town_code
    user_town_code = message_text(get_message)
    # 基本檢查是否為5-7個字，以及確認是否有出現'縣市鄉鎮市區'字樣
    if not user_town_code:
        msg = "⚠️請檢查欲查詢水情之行政區的錯字或遺漏字，並符合5至7個字。\n例如: 嘉義縣阿里山鄉、臺東縣成功鎮、南投縣南投市、臺中市西區。\n\n⚠️或是在介面左下方「＋」選擇位置資訊，並根據您的所在位置或是指定位置發送給我。"
    else:
        # e.g. {"河川":"str", "雨勢":"str", "水庫":"str"}
        water_condition = input_text(user_town_code)
        msg = f"您輸入的是: \n{get_message}\n\n此區域的水情狀況⬇\n\n河川: \n{water_condition['water']}\n\n雨勢: \n{water_condition['rain']}\n\n水庫: \n{water_condition['reservoir']}"
    # Send To Line
    reply = TextSendMessage(
        text=msg)
    line_bot_api.reply_message(event.reply_token, reply)


@handler.add(MessageEvent, message=LocationMessage)  # 根據行政區和經緯度判斷warning
def handle_message_location(event):
    get_message = event.message.address
    latitude = event.message.latitude
    longitude = event.message.longitude
    # get user_town_code
    user_town_code = message_location(get_message)
    if not user_town_code:
        msg = "⚠️請重新發送位置資訊。"
    else:
        water_condition = input_location(user_town_code, latitude, longitude)
        msg = f"您輸入的是: \n{get_message}\n\n此區域的水情狀況⬇\n\n河川: \n{water_condition['water']}\n\n雨勢: \n{water_condition['rain']}\n\n水庫: \n{water_condition['reservoir']}"
    # Send To Line
    reply = TextSendMessage(
        text=msg)
    line_bot_api.reply_message(event.reply_token, reply)


if __name__ == "__main__":
    # In debug mode, Flask's reloader will load the flask app twice
    app.run(use_reloader=False)
