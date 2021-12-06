from os import name
import requests
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash


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


# init server
app = Flask(__name__)
app.config['DEBUG'] = True


# initial route
@app.route('/', methods=['GET'])
def index():
    return render_template("index.html")


# search route
@app.route('/search', methods=['GET'])
def search_get():
    return render_template("search.html")


@app.route("/search/result", methods=['POST'])
def search_request():
    if request.method == 'POST':
        city = request.values["city"]
        citycode = cityNameToCode(city)
        water_stations = get_water_station_basic(citycode)
        return render_template("result.html", water_stations=water_stations)


if __name__ == "__main__":
    app.run()


# @app.route("/search/<city>", methods=['GET'])
# def search_result(water_stations):


# water_station_basic = get_water_station_basic()
# water_realtime = get_water_realtime()
#current_time = datetime.today()
# for i in water_station_basic:
#     try:
#         if "新北市" in i["Address"]:
#             print(i)
#     except:
#         continue
# print(water_realtime)
# print(len(water_realtime))
