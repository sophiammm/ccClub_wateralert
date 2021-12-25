import os
from flask import Flask, abort, request, render_template, jsonify, g
from flask_mail import Mail, Message
from wtforms import SelectField
from flask_wtf import FlaskForm
from db_operator.read_from_db import check_warn, read_city, read_town_by_city_code, read_address_by_town_code, check_warn
from db_operator.update import update_user_location
from gps_address import gps_to_address
from auth import bp


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
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 587
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False


# init server
def create_app():
    app = Flask(__name__)
    app.config.from_object(Config())
    # 測試階段先開啟DEBUG, 正式運行要關掉
    app.config['DEBUG'] = True
    return app


app = create_app()


# set mail function
mail = Mail(app)


def send_warn(user_email, info):
    msg = Message('Water Alert', sender=os.getenv("MAIL_USERNAME"),
                  recipients=[user_email])
    msg.body = f"{info}"
    try:
        mail.send(msg)
        return "Sent"
    except Exception as e:
        print(e)
        return "Error"


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


# test mail
@app.route("/mail")
def test():
    return send_warn()


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
        return render_template("result.html", address=address, water_warn=water_warn, rain_warn=rain_warn, reservoir_warn=reservoir_warn)


@handler.add(MessageEvent, message=TextMessage)  # 根據行政區判斷Warning
def handle_message_text(event):
    get_message = event.message.text
    # Send To Line
    reply = TextSendMessage(
        text=input_text(get_message))
    line_bot_api.reply_message(event.reply_token, reply)


@handler.add(MessageEvent, message=LocationMessage)  # 根據行政區和經緯度判斷warning
def handle_message_location(event):
    get_message = event.message.address
    latitude = event.message.latitude
    longitude = event.message.longitude
    # Send To Line
    reply = TextSendMessage(
        text=input_location(get_message, latitude, longitude))
    line_bot_api.reply_message(event.reply_token, reply)


if __name__ == "__main__":
    # In debug mode, Flask's reloader will load the flask app twice
    app.run(use_reloader=False)
