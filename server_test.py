import requests
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_apscheduler import APScheduler
from db_operator.base_manager import PostgresBaseManager
from db_operator.save_from_wra import save_reservoir_warning, save_rain_warning, save_water_warning, truncate_table
from db_operator.update_from_wra import update_rain_warning, update_water_warning, update_reservoir_warning
from db_operator.read_from_db import read_table
from timestamp import stamp_to_date


# set configuration values
class Config:
    SCHEDULER_API_ENABLED = True
    SCHEDULER_TIMEZONE = "Asia/Taipei"  # <========== 設置時區, 時區不一致可能會導致任務時間出錯


# init server
app = Flask(__name__)
app.config.from_object(Config())
# 測試階段先開啟DEBUG, 正式運行要關掉
app.config['DEBUG'] = True


# functions to get data from wra api
def cityNameToCodeAndEn(cityCN):
    url = f"https://fhy.wra.gov.tw/WraApi/v1/Basic/City?$filter=CityName_Ch%20eq%20'{cityCN}'"
    re = requests.get(url).json()
    return {"code": re[0]["CityCode"], "en": re[0]["CityName_En"], "ch": re[0]["CityName_Ch"]}


def townNameToCode(cityEn, town):
    url = f"https://fhy.wra.gov.tw/WraApi/v1/Basic/{cityEn}/Town?$filter=TownName%20eq%20'{town}'"
    re = requests.get(url).json()
    try:
        result = re[0]["TownCode"]
    except:
        result = "No Data"
    return result


def getWaterWarning(cityCode):
    url = f"https://fhy.wra.gov.tw/WraApi/v1/Water/Warning?$filter=CityCode%20eq%20'{cityCode}'"
    re = requests.get(url).json()
    if re != []:
        result = re
    else:
        result = "No warning."
    return result


def getWaterStationTown(town=""):
    if town == "":
        url = "https://fhy.wra.gov.tw/WraApi/v1/Water/Station"
    else:
        url = f"https://fhy.wra.gov.tw/WraApi/v1/Water/Station?$filter=contains(Address%2C'{town}')"
    re = requests.get(url).json()
    return re


def getWaterStationCity(CityCode=""):
    if CityCode == "":
        url = "https://fhy.wra.gov.tw/WraApi/v1/Water/Station"
    else:
        url = f"https://fhy.wra.gov.tw/WraApi/v1/Water/Station?$filter=CityCode%20eq%20'{CityCode}'"
    re = requests.get(url).json()
    return re


def getWaterRealtime(StationNo):
    re = requests.get(
        "https://fhy.wra.gov.tw/WraApi/v1/Water/RealTimeInfo").json()
    return re


# initial route
@ app.route('/', methods=['GET'])
def index():
    return render_template("index.html")


# search route
@ app.route('/search', methods=['GET'])
def search_get():
    return render_template("search.html")


@ app.route("/result", methods=['POST'])
def search_request():
    if request.method == 'POST':
        city = request.values["city"]
        citycode = cityNameToCodeAndEn(city)["code"]
        water_stations = getWaterStationCity(citycode)
        return render_template("result.html", water_stations=water_stations)


# check warn route
@ app.route("/warn", methods=['GET'])
def warn_get():
    waterWarns = read_table("Water_Warning")
    for waterWarn in waterWarns:
        waterWarn["APIupdateTime"] = stamp_to_date(waterWarn["APIupdateTime"])
    rainWarns = read_table("Rain_Warning")
    for rainWarn in rainWarns:
        rainWarn["APIupdateTime"] = stamp_to_date(rainWarn["APIupdateTime"])
    reservoirWarns = read_table("Reservoir_Warning")
    for reservoirWarn in reservoirWarns:
        reservoirWarn["APIupdateTime"] = stamp_to_date(
            reservoirWarn["APIupdateTime"])
        reservoirWarns["NextSpillTime"] = stamp_to_date(
            reservoirWarns["NextSpillTime"])
    return render_template("warn.html", waterWarns=waterWarns, rainWarns=rainWarns, reservoirWarns=reservoirWarns)


# select box test
@ app.route("/select")
def select():
    return render_template("select_box.html")


# def showWarn():
#     # Get data from WRA API test
#     city = cityNameToCodeAndEn("新北市")
#     cityCode = city["code"]
#     cityEn = city["en"]
#     town = "汐止區"
#     print(getWaterWarning(cityCode))
#     print(getWaterStationTown(town))


if __name__ == "__main__":

    # initialize scheduler
    scheduler = APScheduler()

    # Add task
    @scheduler.task('interval', id='save_warn', seconds=15, misfire_grace_time=900)
    def save_warn_from_wra():
        print('Job 1 executed')
        # truncate_table("Rain_Warning")
        # truncate_table("Water_Warning")
        # truncate_table("Reservoir_Warning")
        # save_rain_warning()
        # save_water_warning()
        # save_reservoir_warning()
        update_rain_warning()
        update_water_warning()
        update_reservoir_warning()

    # if you don't wanna use a config, you can set options here:
    # scheduler.api_enabled = True
    scheduler.init_app(app)

    scheduler.start()

    # In debug mode, Flask's reloader will load the flask app twice
    app.run(use_reloader=False)
