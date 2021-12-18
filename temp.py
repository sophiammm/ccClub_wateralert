import requests
from gps_address import address_to_gps

reservoir_station_api = "https://fhy.wra.gov.tw/WraApi/v1/Reservoir/Station"
origin = requests.get(reservoir_station_api).json()


temp = []
suc = []
fail = []
for info in origin:
    try:
        info["Latitude"]
    # 沒有經緯度的水庫
    except:
        temp.append(info)
        # 找得到經緯度
        if address_to_gps(info["StationName"]):
            suc.append(info)
        # 找不到經緯度
        else:
            fail.append(info)
print(temp)
print("*"*150)
print(suc)
print("*"*150)
print(fail)
print("*"*150)
print(len(temp), len(suc), len(fail))
