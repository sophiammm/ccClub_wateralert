from auth import bp
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, g
from wtforms import SelectField
import os
from flask_wtf import FlaskForm
from flask_apscheduler import APScheduler
from db_operator.save_from_wra import save_reservoir_warning, save_rain_warning, save_water_warning, truncate_table
from db_operator.update_from_wra import update_rain_warning, update_water_warning, update_reservoir_warning, update_user_location
from db_operator.read_from_db import read_table, read_city, read_town_by_city_code, read_address_by_town_code, check_warn
from gps_address import gps_to_address
from timestamp import stamp_to_date


# set configuration values
class Config:
    SCHEDULER_API_ENABLED = True
    SCHEDULER_TIMEZONE = "Asia/Taipei"  # <========== 設置時區, 時區不一致可能會導致任務時間出錯
    SECRET_KEY = "jhihiogspoihgfaphga"


# init server
app = Flask(__name__)
app.config.from_object(Config())
# 測試階段先開啟DEBUG, 正式運行要關掉
app.config['DEBUG'] = True


class AddressForm(FlaskForm):
    city = SelectField("city", choices=[])
    town = SelectField("town", choices=[])


# initial route
@ app.route('/', methods=['GET'])
def index():
    return render_template("index.html")


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


if __name__ == "__main__":

    # # initialize scheduler
    # scheduler = APScheduler()

    # # Add task
    # @scheduler.task('interval', id='save_warn', seconds=15, misfire_grace_time=120)
    # def save_warn_from_wra():
    #     print('task executed at ' + str(datetime.now()))
    #     sys.stdout.flush()
    #     # truncate_table("Rain_Warning")
    #     # truncate_table("Water_Warning")
    #     # truncate_table("Reservoir_Warning")
    #     # save_rain_warning()
    #     # save_water_warning()
    #     # save_reservoir_warning()
    #     update_rain_warning()
    #     update_water_warning()
    #     update_reservoir_warning()

    # # if you don't wanna use a config, you can set options here:
    # # scheduler.api_enabled = True
    # scheduler.init_app(app)

    # scheduler.start()

    # In debug mode, Flask's reloader will load the flask app twice
    app.run(use_reloader=False)
