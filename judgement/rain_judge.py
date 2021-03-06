import sys
sys.path.append("../")

from db_operator.read_from_db import read
from gps_address import in_range

def rain_judge_by_town(user_town_code):
    read_rain_warn_sql = "SELECT * FROM Rain_Warning"
    # staionNo, townCode, APItime, DBtime, warninglevel [1, 2]
    datas = read(read_rain_warn_sql)
    result = []
    warnings = []
    for data in datas:
        townCode = data[1]
        level = data[4]
        if user_town_code == townCode:
            warnings.append(level)
    
    warnings.sort(reverse = True)
    if warnings == []:
        msg = {"warningLevel": 0}
        result.append(msg)
    else:
        msg = {"warningLevel": warnings[0]}
        result.append(msg)

    return result
    # 0: 沒有警戒; 1: 一級警戒; 2: 二級警戒


def rain_judge_by_location(latitude, longitude):
    read_rain_warn_sql = "SELECT * FROM Rain_Warning"
    # staionNo, townCode, APItime, DBtime, warninglevel [1, 2]
    datas = read(read_rain_warn_sql)
    # staionNo, latitude, longitude
    read_rain_station_sql = "SELECT * FROM Rain_Station"
    stations = read(read_rain_station_sql)
    near_stations = []
    for station in stations:
        user_location = (latitude, longitude)
        station_location = (station[1], station[2])
        is_close = in_range(user_location, station_location, 5)
        stationno = station[0]
        if is_close:
            near_stations.append(stationno)

    result = []
    warnings = []
    for i in range(len(near_stations)):
        for j in range(len(datas)):
            if near_stations[i] == datas[j][0]:
                warnings.append(datas[j][4])
    
    warnings.sort(reverse = True)
    if warnings == []:
        msg = {"warningLevel": 0}
        result.append(msg)
    else:
        msg = {"warningLevel": warnings[0]}
        result.append(msg)

    return result
    # 0: 沒有警戒; 1: 一級警戒; 2: 二級警戒
