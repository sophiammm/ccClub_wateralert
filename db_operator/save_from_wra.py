import requests
from psycopg2 import extras
from db_operator.base_manager import PostgresBaseManager
from datetime import datetime
from timestamp import date_to_stamp
from gps_address import address_to_gps


def save_city_town():
    postgres_manager = PostgresBaseManager()
    cur = postgres_manager.conn.cursor()
    city_api = "https://fhy.wra.gov.tw/WraApi/v1/Basic/City"
    city_info = requests.get(city_api).json()
    for info in city_info:
        cityCode = info["CityCode"]
        cityName = info["CityName_Ch"]
        cityName_En = info["CityName_En"]

        town_api = f"https://fhy.wra.gov.tw/WraApi/v1/Basic/{cityName_En}/Town"
        town_info = requests.get(town_api).json()
        same_city_rows = []
        for info in town_info:
            townCode = info["TownCode"]
            townName = info["TownName"]
            same_city_rows.append((cityCode, cityName, townCode, townName))

        sql = "INSERT INTO City_Town (cityCode, cityName, townCode, townName) VALUES %s"
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


def save_rain_station():
    postgres_manager = PostgresBaseManager()
    cur = postgres_manager.conn.cursor()
    rain_station_api = "https://fhy.wra.gov.tw/WraApi/v1/Rain/Station"
    rain_station_info = requests.get(rain_station_api).json()
    rows = []
    for info in rain_station_info:
        try:
            stationNo = info["StationNo"]
            latitude = info["Latitude"]
            longitude = info["Longitude"]
        except:
            stationName = info["StationName"]
            loc = address_to_gps(stationName)
            if loc:
                latitude = loc[0]
                longitude = loc[1]
            else:
                continue
        rows.append((stationNo, latitude, longitude))

    sql = "INSERT INTO Rain_Station (stationNo, latitude, longitude) VALUES %s"
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


def save_water_station():
    postgres_manager = PostgresBaseManager()
    cur = postgres_manager.conn.cursor()
    water_station_api = "https://fhy.wra.gov.tw/WraApi/v1/Water/Station"
    water_station_info = requests.get(water_station_api).json()
    rows = []
    for info in water_station_info:
        stationNo = info["StationNo"]
        basinName = info["BasinName"]
        try:

            latitude = info["Latitude"]
            longitude = info["Longitude"]
        except:
            stationName = info["StationName"]
            loc = address_to_gps(stationName)
            if loc:
                latitude = loc[0]
                longitude = loc[1]
            else:
                continue
        rows.append((stationNo, basinName, latitude, longitude))

    sql = "INSERT INTO Water_Station (stationNo, basinName, latitude, longitude) VALUES %s"
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

    sql = "INSERT INTO Reservoir_Warning (stationNo, townCode, APIupdateTime, DBupdateTime, nextSpillTime, status) VALUES %s"
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
    rows = []
    for info in reservoir_station_info:
        stationNo = info["StationNo"]
        stationName = info["StationName"]
        rows.append((stationNo, stationName))

    sql = "INSERT INTO Reservoir_Station (stationNo, stationName) VALUES %s"
    try:
        extras.execute_values(cur, sql, rows)
    except Exception as e:
        print("Save failed.")
        print(e)
    postgres_manager.conn.commit()
    cur.close()
    postgres_manager.close_connection()
    print("Operation completed")


def save_reservoir_affectedarea():
    postgres_manager = PostgresBaseManager()
    cur = postgres_manager.conn.cursor()
    reservoir_affectedarea_api = "https://fhy.wra.gov.tw/WraApi/v1/Reservoir/AffectedArea"
    reservoir_affectedarea_info = requests.get(
        reservoir_affectedarea_api).json()
    rows = []
    for info in reservoir_affectedarea_info:
        try:
            stationNo = info["StationNo"]
            townCode = info["TownCode"]
        except:
            continue
        rows.append((stationNo, townCode))

    sql = "INSERT INTO Reservoir_AffectedArea (stationNo, townCode) VALUES %s"
    try:
        extras.execute_values(cur, sql, rows)
    except Exception as e:
        print("Save failed.")
        print(e)
    postgres_manager.conn.commit()
    cur.close()
    postgres_manager.close_connection()
    print("Operation completed")


# ???????????????
def save_fake_to_water_warning():
    postgres_manager = PostgresBaseManager()
    cur = postgres_manager.conn.cursor()
    cur.execute("""
        INSERT INTO water_warning (stationno, towncode, warninglevel)
        VALUES (%s, %s, %s);
        """,
                ('1420H053', '6601000', 1))
    postgres_manager.conn.commit()
    cur.close()
    postgres_manager.close_connection()


def save_fake_to_rain_warning(stationNo="00H810", townCode="1000813", warningLevel=2):
    postgres_manager = PostgresBaseManager()
    cur = postgres_manager.conn.cursor()
    try:
        cur.execute("""
            INSERT INTO rain_warning (stationno, towncode, warningLevel)
            VALUES (%s, %s, %s);
            """,
                    (stationNo, townCode, warningLevel))
    except Exception as e:
        print("Insert failed.")
        print(e)
    postgres_manager.conn.commit()
    cur.close()
    postgres_manager.close_connection()


def save_fake_to_reservoir_warning(stationNo="30501", townCode="6700600", nextSpillTime="2021-12-27 12:08", status="'0: ????????????'"):
    postgres_manager = PostgresBaseManager()
    cur = postgres_manager.conn.cursor()
    nextSpillStamp = date_to_stamp(nextSpillTime)
    try:
        cur.execute("""
            INSERT INTO reservoir_warning (stationno, townCode, nextSpillTime, status)
            VALUES (%s, %s, %s, %s);
            """,
                    (stationNo, townCode, nextSpillStamp, status))
    except Exception as e:
        print("Insert failed.")
        print(e)
    postgres_manager.conn.commit()
    cur.close()
    postgres_manager.close_connection()
    print("Operation completed")


# ??????table?????????
def truncate_table(table):
    postgres_manager = PostgresBaseManager()
    cur = postgres_manager.conn.cursor()
    try:
        cur.execute(f" TRUNCATE TABLE {table}")
        postgres_manager.conn.commit()
    except Exception as e:
        print("Truncate failed.")
        print(e)
    cur.close()
    postgres_manager.close_connection()
    print("Operation completed")
