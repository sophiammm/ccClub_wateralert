import requests
from psycopg2 import extras
from datetime import datetime
from db_operator.base_manager import PostgresBaseManager
from timestamp import date_to_stamp


def update_rain_warning():
    postgres_manager = PostgresBaseManager()
    cur = postgres_manager.conn.cursor()
    rain_warn_api = "https://fhy.wra.gov.tw/WraApi/v1/Rain/Warning"
    rain_warn_info = requests.get(rain_warn_api).json()
    rows = []
    for info in rain_warn_info:
        stationNo = info["StationNo"]
        townCode = info["TownCode"]
        APIupdateTime = date_to_stamp(info["Time"])
        DBupdateTime = date_to_stamp(str(datetime.now()))
        warningLevel = info["WarningLevel"]
        rows.append((stationNo, townCode, APIupdateTime,
                    DBupdateTime, warningLevel))

    sql = "INSERT INTO Rain_Warning (stationNo, townCode, APIupdateTime, DBupdateTime, warningLevel) VALUES %s ON conflict(stationNo) DO UPDATE SET warninglevel = EXCLUDED.warninglevel, APIupdateTime=EXCLUDED.APIupdateTime, DBupdateTime=EXCLUDED.DBupdateTime;"
    try:
        extras.execute_values(cur, sql, rows)
    except Exception as e:
        print("Save failed.")
        print(e)
    postgres_manager.conn.commit()
    cur.close()
    postgres_manager.close_connection()
    print("Operation completed")


def update_water_warning():
    postgres_manager = PostgresBaseManager()
    cur = postgres_manager.conn.cursor()
    water_warn_api = "https://fhy.wra.gov.tw/WraApi/v1/Water/Warning"
    water_warn_info = requests.get(water_warn_api).json()
    rows = []
    for info in water_warn_info:
        stationNo = info["StationNo"]
        townCode = info["TownCode"]
        APIupdateTime = date_to_stamp(info["Time"])
        DBupdateTime = date_to_stamp(str(datetime.now()))
        warningLevel = info["WarningLevel"]
        rows.append((stationNo, townCode, APIupdateTime,
                     DBupdateTime, warningLevel))

    sql = "INSERT INTO Water_Warning (stationNo, townCode, APIupdateTime, DBupdateTime, warningLevel) VALUES %s ON conflict(stationNo) DO UPDATE SET warninglevel = EXCLUDED.warninglevel, APIupdateTime=EXCLUDED.APIupdateTime, DBupdateTime=EXCLUDED.DBupdateTime;"
    try:
        extras.execute_values(cur, sql, rows)
    except Exception as e:
        print("Save failed.")
        print(e)
    postgres_manager.conn.commit()
    cur.close()
    postgres_manager.close_connection()
    print("Operation completed")


def update_reservoir_warning():
    postgres_manager = PostgresBaseManager()
    cur = postgres_manager.conn.cursor()
    reservoir_warn_api = "https://fhy.wra.gov.tw/WraApi/v1/Reservoir/Warning"
    reservoir_warn_info = requests.get(reservoir_warn_api).json()
    rows = []
    for info in reservoir_warn_info:
        try:
            stationNo = info["StationNo"]
            townCode = info["TownCode"]
            APIupdateTime = date_to_stamp(info["Time"])
            DBupdateTime = date_to_stamp(str(datetime.now()))
            nextSpillTime = date_to_stamp(info["NextSpillTime"])
            status = info["Status"]
        except:
            continue
        rows.append((stationNo, townCode, APIupdateTime,
                    DBupdateTime, nextSpillTime, status))

    sql = "INSERT INTO Reservoir_Warning (stationNo, townCode, APIupdateTime, DBupdateTime, nextSpillTime, status) VALUES %s ON conflict(stationNo) DO UPDATE SET nextSpillTime=EXCLUDED.nextSpillTime, status=EXCLUDED.status, APIupdateTime=EXCLUDED.APIupdateTime, DBupdateTime=EXCLUDED.DBupdateTime;"
    try:
        extras.execute_values(cur, sql, rows)
    except Exception as e:
        print("Save failed.")
        print(e)
    postgres_manager.conn.commit()
    cur.close()
    postgres_manager.close_connection()
    print("Operation completed")


def update_user_location(id, lat, lon):
    postgres_manager = PostgresBaseManager()
    cur = postgres_manager.conn.cursor()
    sql = "INSERT INTO usrLocation (ownerID, latitude, longitude) VALUES %s ON conflict(ownerID) DO UPDATE SET latitude=EXCLUDED.latitude, longitude=EXCLUDED.longitude;"
    rows = [(id, lat, lon)]
    try:
        extras.execute_values(cur, sql, rows)
    except Exception as e:
        print("Save failed.")
        print(e)
    postgres_manager.conn.commit()
    cur.close()
    postgres_manager.close_connection()
    print("Operation completed")
