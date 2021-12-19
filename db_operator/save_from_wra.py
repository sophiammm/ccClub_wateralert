import requests
from datetime import datetime
from db_operator.base_manager import PostgresBaseManager
from psycopg2 import extras
from timestamp import date_to_stamp
from gps_address import address_to_gps


def save_city_town():
    postgres_manager = PostgresBaseManager()
    cur = postgres_manager.conn.cursor()
    city_api = "https://fhy.wra.gov.tw/WraApi/v1/Basic/City"
    city_info = requests.get(city_api).json()
    for info in city_info:
        cityID = info["CityCode"]
        cityName = info["CityName_Ch"]
        cityName_En = info["CityName_En"]

        town_api = f"https://fhy.wra.gov.tw/WraApi/v1/Basic/{cityName_En}/Town"
        town_info = requests.get(town_api).json()
        same_city_rows = []
        for info in town_info:
            print(info)
            townID = info["TownCode"]
            townName = info["TownName"]
            same_city_rows.append((cityID, cityName, townID, townName))

        sql = "INSERT INTO City_Town (cityID, cityName, townID, townName) VALUES %s"
        try:
            extras.execute_values(cur, sql, same_city_rows)
        except Exception as e:
            print("Save failed.")
            print(e)
    postgres_manager.conn.commit()
    cur.close()
    postgres_manager.close_connection()
    print("Operation completed")


def save_rain_warning():
    postgres_manager = PostgresBaseManager()
    cur = postgres_manager.conn.cursor()
    rain_warn_api = "https://fhy.wra.gov.tw/WraApi/v1/Rain/Warning"
    rain_warn_info = requests.get(rain_warn_api).json()
    rows = []
    for info in rain_warn_info:
        print(info)
        stationNo = info["StationNo"]
        townCode = info["TownCode"]
        APIupdateTime = date_to_stamp(info["Time"])
        DBupdateTime = date_to_stamp(str(datetime.now()))
        warningLevel = info["WarningLevel"]
        rows.append((stationNo, townCode, APIupdateTime,
                    DBupdateTime, warningLevel))

    sql = "INSERT INTO Rain_Warning (stationNo, townCode, APIupdateTime, DBupdateTime, warningLevel) VALUES %s"
    try:
        extras.execute_values(cur, sql, rows)
    except Exception as e:
        print("Save failed.")
        print(e)
    postgres_manager.conn.commit()
    cur.close()
    postgres_manager.close_connection()
    print("Operation completed")


def save_water_warning():
    postgres_manager = PostgresBaseManager()
    cur = postgres_manager.conn.cursor()
    water_warn_api = "https://fhy.wra.gov.tw/WraApi/v1/Water/Warning"
    water_warn_info = requests.get(water_warn_api).json()
    rows = []
    for info in water_warn_info:
        print(info)
        stationNo = info["StationNo"]
        townCode = info["TownCode"]
        APIupdateTime = date_to_stamp(info["Time"])
        DBupdateTime = date_to_stamp(str(datetime.now()))
        warningLevel = info["WarningLevel"]
        rows.append((stationNo, townCode, APIupdateTime,
                     DBupdateTime, warningLevel))

    sql = "INSERT INTO Water_Warning (stationNo, townCode, APIupdateTime, DBupdateTime, warningLevel) VALUES %s"
    try:
        extras.execute_values(cur, sql, rows)
    except Exception as e:
        print("Save failed.")
        print(e)
    postgres_manager.conn.commit()
    cur.close()
    postgres_manager.close_connection()
    print("Operation completed")


def save_reservoir_warning():
    postgres_manager = PostgresBaseManager()
    cur = postgres_manager.conn.cursor()
    reservoir_warn_api = "https://fhy.wra.gov.tw/WraApi/v1/Reservoir/Warning"
    reservoir_warn_info = requests.get(reservoir_warn_api).json()
    rows = []
    for info in reservoir_warn_info:
        print(info)
        try:
            stationNo = info["StationNo"]
            townCode = info["TownCode"]
            APIupdateTime = date_to_stamp(info["Time"])
            DBupdateTime = date_to_stamp(str(datetime.now()))
            nextSpillTime = date_to_stamp(info["NextSpillTime"])
        except:
            continue
        rows.append((stationNo, townCode, APIupdateTime,
                    DBupdateTime, nextSpillTime))

    sql = "INSERT INTO Reservoir_Warning (stationNo, townCode, APIupdateTime, DBupdateTime, nextSpillTime) VALUES %s"
    try:
        extras.execute_values(cur, sql, rows)
    except Exception as e:
        print("Save failed.")
        print(e)
    postgres_manager.conn.commit()
    cur.close()
    postgres_manager.close_connection()
    print("Operation completed")


def save_rain_station():
    postgres_manager = PostgresBaseManager()
    cur = postgres_manager.conn.cursor()
    rain_station_api = "https://fhy.wra.gov.tw/WraApi/v1/Rain/Station"
    rain_station_info = requests.get(rain_station_api).json()
    rows = []
    for info in rain_station_info:
        print(info)
        try:
            stationNo = info["StationNo"]
            stationName = info["StationName"]
            DBupdateTime = date_to_stamp(str(datetime.now()))
            latitude = info["Latitude"]
            longitude = info["Longitude"]
        except:
            continue
        rows.append((stationNo, stationName, latitude,
                    longitude, DBupdateTime))

    sql = "INSERT INTO Rain_Station (stationNo, stationName, latitude, longitude, DBupdateTime) VALUES %s"
    try:
        extras.execute_values(cur, sql, rows)
    except Exception as e:
        print("Save failed.")
        print(e)
    postgres_manager.conn.commit()
    cur.close()
    postgres_manager.close_connection()
    print("Operation completed")


def save_water_station():
    postgres_manager = PostgresBaseManager()
    cur = postgres_manager.conn.cursor()
    water_station_api = "https://fhy.wra.gov.tw/WraApi/v1/Water/Station"
    water_station_info = requests.get(water_station_api).json()
    rows = []
    for info in water_station_info:
        print(info)
        stationNo = info["StationNo"]
        stationName = info["StationName"]
        DBupdateTime = date_to_stamp(str(datetime.now()))
        try:
            latitude = info["Latitude"]
            longitude = info["Longitude"]
        except:
            loc = address_to_gps(stationName)
            if loc:
                latitude = loc[0]
                longitude = loc[1]
            else:
                continue
        rows.append((stationNo, stationName, latitude,
                    longitude, DBupdateTime))

    sql = "INSERT INTO Water_Station (stationNo, stationName, latitude, longitude, DBupdateTime) VALUES %s"
    try:
        extras.execute_values(cur, sql, rows)
    except Exception as e:
        print("Save failed.")
        print(e)
    postgres_manager.conn.commit()
    cur.close()
    postgres_manager.close_connection()
    print("Operation completed")


def save_reservoir_station():
    postgres_manager = PostgresBaseManager()
    cur = postgres_manager.conn.cursor()
    reservoir_station_api = "https://fhy.wra.gov.tw/WraApi/v1/Reservoir/Station"
    reservoir_station_info = requests.get(reservoir_station_api).json()
    print(len(reservoir_station_info))
    rows = []
    for info in reservoir_station_info:
        # print(info)
        stationNo = info["StationNo"]
        stationName = info["StationName"]
        DBupdateTime = date_to_stamp(str(datetime.now()))
        try:
            latitude = info["Latitude"]
            longitude = info["Longitude"]
        except:
            print(info)
            loc = address_to_gps(stationName)
            if loc:
                latitude = loc[0]
                longitude = loc[1]
            else:
                continue
        rows.append((stationNo, stationName, latitude,
                    longitude, DBupdateTime))

    sql = "INSERT INTO Reservoir_Station (stationNo, stationName, latitude, longitude, DBupdateTime) VALUES %s"
    extras.execute_values(cur, sql, rows)
    postgres_manager.conn.commit()
    cur.close()
    postgres_manager.close_connection()
    print("Operation completed")


def truncate_table(table):
    postgres_manager = PostgresBaseManager()
    cur = postgres_manager.conn.cursor()
    cur.execute(f" TRUNCATE TABLE {table}")
    postgres_manager.conn.commit()
    cur.close()
    postgres_manager.close_connection()
    print("Operation completed")
