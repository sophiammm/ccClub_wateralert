import requests
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_apscheduler import APScheduler


# set configuration values
class Config:
    SCHEDULER_API_ENABLED = True
    SCHEDULER_TIMEZONE = "Asia/Taipei"  # <========== 設置時區, 時區不一致可能會導致任務時間出錯


# init server
app = Flask(__name__)
app.config.from_object(Config())
app.config['DEBUG'] = True


def cityNameToCode(s):
    url = f"https://fhy.wra.gov.tw/WraApi/v1/Basic/City?$filter=CityName_Ch%20eq%20'{s}'"
    re = requests.get(url).json()
    return re[0]["CityCode"]


def get_water_station_basic(CityCode=""):
    if CityCode == "":
        url = "https://fhy.wra.gov.tw/WraApi/v1/Water/Station"
    else:
        url = f"https://fhy.wra.gov.tw/WraApi/v1/Water/Station?$filter=CityCode%20eq%20'{CityCode}'"
    re = requests.get(url).json()
    return re


def get_water_realtime(StationNo):
    re = requests.get(
        "https://fhy.wra.gov.tw/WraApi/v1/Water/RealTimeInfo").json()
    return re


# initial route
@app.route('/', methods=['GET'])
def index():
    return render_template("index.html")


# search route
@app.route('/search', methods=['GET'])
def search_get():
    return render_template("search.html")


@app.route("/result", methods=['POST'])
def search_request():
    if request.method == 'POST':
        city = request.values["city"]
        citycode = cityNameToCode(city)
        water_stations = get_water_station_basic(citycode)
        return render_template("result.html", water_stations=water_stations)


if __name__ == "__main__":

    # initialize scheduler
    scheduler = APScheduler()

    # Add task
    @scheduler.task('interval', id='do_job_1', seconds=3, misfire_grace_time=900)
    def job1():
        print('Job 1 executed')

    # if you don't wanna use a config, you can set options here:
    # scheduler.api_enabled = True
    scheduler.init_app(app)

    scheduler.start()

    # In debug mode, Flask's reloader will load the flask app twice
    app.run(use_reloader=False)
