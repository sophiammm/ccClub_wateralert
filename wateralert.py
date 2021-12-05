import requests
from bs4 import BeautifulSoup
from datetime import datetime

user_town_time = input().split(",")
user_town = user_town_time[0]
user_time_str = user_town_time[1]
user_time = datetime.strptime(user_time_str, '%Y-%m-%d %H:%M:%S')
# print(user_time, type(user_time))

alert = "no alert"

# # 雨量站
# rainstation_api = "https://fhy.wra.gov.tw/WraApi/v1/Rain/Station"
# station_info = requests.get(rainstation_api).json()
# # print(station_info)
# for station in station_info:
#     city = station["CityCode"]
#     if user_town == city:
#         return 

# 水位警示
water_warning_api = "https://fhy.wra.gov.tw/WraApi/v1/Water/Warning"
water_info = requests.get(water_warning_api).json()
for water in water_info:
    town = water["TownCode"]
    warning = water["WarningLevel"]
    if user_town == town:
        alert = warning

# 淹水警示
flood_warning_api = "https://fhy.wra.gov.tw/WraApi/v1/Rain/Warning"
flood_info = requests.get(flood_warning_api).json()
for flood in flood_info:
    town = flood["TownCode"]
    warning = flood["WarningLevel"]
    if user_town == town:
        alert = warning

# 水庫警示
reservoir_warning_api = "https://fhy.wra.gov.tw/WraApi/v1/Reservoir/Warning"
reservoir_info = requests.get(reservoir_warning_api).json()
for reservoir in reservoir_info:
    town = reservoir["TownCode"]
    release = reservoir["Status"]
    if user_town == town and release == "1":
        alert = warning

print(alert)




