from flask import Flask, render_template, jsonify, request
from wtforms import SelectField
from flask_wtf import FlaskForm
from db_operator.read_from_db import read_city, read_town_by_city_code, read_address_by_town_code, check_warn
from gps_address import gps_to_address


class Config:
    SCHEDULER_API_ENABLED = True
    SCHEDULER_TIMEZONE = "Asia/Taipei"  # <========== 設置時區, 時區不一致可能會導致任務時間出錯
    SECRET_KEY = "thisissecret"


app = Flask(__name__)
app.config.from_object(Config())


class Form(FlaskForm):
    city = SelectField("city", choices=[])
    town = SelectField("town", choices=[])


@ app.route("/")
def index():
    return render_template("index.html")


@ app.route("/location", methods=["GET", "POST"])
def test():
    if request.method == "GET":
        return render_template("location.html")
    if request.method == "POST":
        data = request.get_json()
        if data == "":
            print("No data")
        else:
            print(data)
            mark = (data["lat"], data["lon"])
            address = gps_to_address(mark)

        return jsonify({"address": address})


@ app.route("/address")
def select():
    form = Form()
    form.city.choices = read_city()
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


if __name__ == "__main__":
    app.run(debug=True)
