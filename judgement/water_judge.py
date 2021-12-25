import sys
sys.path.append("../")

from db_operator.read_from_db import read, read_water_station
from gps_address import in_range
    

def water_judge_by_town(user_town_code):
    read_water_warn_sql = "SELECT stationNo, townCode, warningLevel FROM Water_Warning;"
    datas = read(read_water_warn_sql)
    warnings = []
    for data in datas:
        stationNo = data[0]
        townCode = data[1]
        level = data[2]
        if user_town_code == townCode:
            warnings.append((stationNo, level))
    final_warnings = {}
    for warning in warnings:
        station_basinName = read_water_station(warning[0])[0][0]
        if final_warnings.__contains__(station_basinName): # 如果final_warnings字典裡包含此流域
            if warning[1] < final_warnings[station_basinName]: # 再判斷其流域的警戒是否比字典裡的嚴重
                final_warnings.update({station_basinName:warning[1]}) # 若更嚴重，就覆蓋字典裡的value
        else: # final_warnings字典裡未包含此流域
            final_warnings.update({station_basinName:warning[1]}) # 新增此流域至字典裡
    
    result = []
    for key in final_warnings:
        msg = {"basinName": key, "warningLevel": final_warnings[key]}
        result.append(msg)

    return result # e.g. [{'basinName': '大甲溪', 'warningLevel': 1}, {'basinName': '秀姑巒溪', 'warningLevel': 2}]
    # 若無警戒，則return []


def water_judge_by_location(latitude, longitude):
    user_location = (latitude, longitude)
    read_water_warn_sql = "SELECT stationNo, warningLevel FROM Water_Warning;"
    warnings = read(read_water_warn_sql)
    final_warnings = {}
    for warning in warnings:
        station_basinName = read_water_station(warning[0])[0][0]
        station_latitude = read_water_station(warning[0])[0][1]
        station_longitude = read_water_station(warning[0])[0][2]
        station_location = (station_latitude, station_longitude)
        if in_range(
            (station_location), (user_location), 5
        ) is True: # 篩選出距離user 5公里內 有warning的測站
            if final_warnings.__contains__(station_basinName): # 如果final_warnings字典裡包含此流域
                if warning[1] < final_warnings[station_basinName]: # 再判斷其流域的警戒是否比字典裡的嚴重
                    final_warnings.update({station_basinName:warning[1]}) # 若更嚴重，就覆蓋字典裡的value
            else: # final_warnings字典裡未包含此流域
                final_warnings.update({station_basinName:warning[1]}) # 新增此流域至字典裡

    result = []
    for key in final_warnings:
        msg = {"basinName": key, "warningLevel": final_warnings[key]}
        result.append(msg)

    return result # e.g. [{'basinName': '大甲溪', 'warningLevel': 1}, {'basinName': '大安溪', 'warningLevel': 2}]
    # 若無警戒，則return []

