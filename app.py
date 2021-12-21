import os
from datetime import datetime
from flask_apscheduler import APScheduler
from wtforms import SelectField
from flask_wtf import FlaskForm
from db_operator.read_from_db import check_warn, read_city, read_town_by_city_code, read_address_by_town_code, check_warn
from db_operator.update_from_wra import update_rain_warning, update_water_warning, update_reservoir_warning
from flask import Flask, abort, request, render_template, jsonify


# https://github.com/line/line-bot-sdk-python
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
# 更新 LocationMessage
from linebot.models import MessageEvent, TextMessage, TextSendMessage, LocationMessage
from linebot_reply import input_text, input_location

# set configuration values


class Config:
    SCHEDULER_API_ENABLED = True
    SCHEDULER_TIMEZONE = "Asia/Taipei"  # <========== 設置時區, 時區不一致可能會導致任務時間出錯
    SECRET_KEY = os.getenv("CSRF_KEY")


# init server
app = Flask(__name__)
app.config.from_object(Config())
# 測試階段先開啟DEBUG, 正式運行要關掉
app.config['DEBUG'] = True

# 定義表格


class Form(FlaskForm):
    city = SelectField("city", choices=[])
    town = SelectField("town", choices=[])


# for linebot
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


@ app.route("/select")
def select():
    form = Form()
    form.city.choices = read_city()
    print(form.city)
    return render_template("select_box.html", form=form)


@ app.route("/select/town/<city_code>")
def town_by_city(city_code):
    towns = read_town_by_city_code(city_code)
    return jsonify({"town_city": towns})


@ app.route("/result", methods=['POST'])
def search_request():
    if request.method == 'POST':
        town_code = request.values["town"]
        address = "".join(read_address_by_town_code(town_code)[0])
        warns = check_warn(town_code)

        def to_string(warns):
            if warns == []:
                return "\nNo warn."
            else:
                msg = "\n"
                for warn in warns:
                    msg += "".join(str(warn))
                return msg
        water_warn = to_string(warns["water"])
        rain_warn = to_string(warns["rain"])
        reservoir_warn = to_string(warns["reservoir"])
        return render_template("result2.html", address=address, water_warn=water_warn, rain_warn=rain_warn, reservoir_warn=reservoir_warn)


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
    line_bot_api.reply_message(event.reply_token, input_location(
        get_message, latitude, longitude))


if __name__ == "__main__":

    # initialize scheduler
    scheduler = APScheduler()

    # Add task
    @scheduler.task('interval', id='save_warn', seconds=600, misfire_grace_time=900)
    def save_warn_from_wra():
        print('task executed')
        update_rain_warning()
        update_water_warning()
        update_reservoir_warning()

    # if you don't wanna use a config, you can set options here:
    # scheduler.api_enabled = True
    scheduler.init_app(app)

    scheduler.start()

    # In debug mode, Flask's reloader will load the flask app twice
    app.run(use_reloader=False)
