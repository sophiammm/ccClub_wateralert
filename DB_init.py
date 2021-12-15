import requests
from datetime import datetime
from DB_basic import PostgresBaseManager
from psycopg2 import extras
from timestamp import dateToStamp


def createCityTownTable():
    postgres_manager = PostgresBaseManager()
    cur = postgres_manager.conn.cursor()
    # cur.execute(
    #     """
    # CREATE TABLE City (
    # cityID varchar(10) PRIMARY key,
    # cityCH varchar(5),
    # cityEN varchar(20)
    # );
    # """)
    # cur.execute(
    #     """
    # CREATE TABLE Town (
    # cityID varchar(10),
    # townID varchar(12) PRIMARY key,
    # townName varchar(5)
    # );
    # """)
    cur.execute(
        """
        CREATE TABLE City_Town (
            cityID varchar(10),
            cityName varchar(5),
            townID varchar(12) PRIMARY key,
            townName varchar(5)
        );
        """
    )
    postgres_manager.conn.commit()
    cur.close()
    postgres_manager.closeConnection()


def saveCityTownData():
    postgres_manager = PostgresBaseManager()
    cur = postgres_manager.conn.cursor()

    city_api = "https://fhy.wra.gov.tw/WraApi/v1/Basic/City"
    city_info = requests.get(city_api).json()
    for info in city_info:
        cityID = info["CityCode"]
        cityName = info["CityName_Ch"]
        cityName_En = info["CityName_En"]

        town_api = "https://fhy.wra.gov.tw/WraApi/v1/Basic/{cityName_En}/Town".format(
            cityName_En=cityName_En)
        town_info = requests.get(town_api).json()
        # try:
        #     cur.execute(
        #         f"INSERT INTO City (cityID, cityCH, cityEN) VALUES ('{cityID}', '{cityName}', '{cityName_En}');")
        # except:
        #     pass
        for info in town_info:
            print(info)
            townID = info["TownCode"]
            townName = info["TownName"]

            # cur.execute(
            #     f"INSERT INTO Town (cityID, townID, townName) VALUES ('{cityID}', '{townID}', '{townName}');")
            cur.execute("""
            INSERT INTO City_Town (cityID, cityName, townID, townName)
            VALUES (%s, %s, %s, %s);
            """,
                        (f"{cityID}", f"{cityName}", f"{townID}", f"{townName}"))
            postgres_manager.conn.commit()
    cur.close()
    postgres_manager.closeConnection()


def createWarningTable():
    postgres_manager = PostgresBaseManager()
    cur = postgres_manager.conn.cursor()
    cur.execute(
        """
        CREATE TABLE Rain_Warning (
        stationNo varchar(12) PRIMARY key,
        townCode varchar(12),
        APIupdateTime int,
        DBupdateTime int,
        warningLevel smallint
        );
        """
    )
    cur.execute(
        """
        CREATE TABLE Rain_Station (
        stationNo varchar(12) PRIMARY key,
        Latitude decimal(10,6),
        Longitude decimal(10,6),
        DBupdateTime int
        );
        """
    )
    cur.execute(
        """
        CREATE TABLE Water_Warning (
        stationNo varchar(12) PRIMARY key,
        townCode varchar(12),
        APIupdateTime int,
        DBupdateTime int,
        warningLevel smallint
        );
        """
    )
    cur.execute(
        """
        CREATE TABLE Water_Station (
        stationNo varchar(12) PRIMARY key,
        Latitude decimal(10,6),
        Longitude decimal(10,6),
        DBupdateTime int
        );
        """
    )
    cur.execute(
        """
        CREATE TABLE Reservoir_Warning (
        stationNo varchar(12) PRIMARY key,
        townCode varchar(12),
        APIupdateTime int,
        DBupdateTime int,
        NextSpillTime int
        );
        """
    )
    cur.execute(
        """
        CREATE TABLE Reservoir_Station (
        stationNo varchar(12) PRIMARY key,
        Latitude decimal(10,6),
        Longitude decimal(10,6),
        DBupdateTime int
        );
        """
    )
    cur.execute(
        """
        CREATE TABLE Reservoir_Affected (
        stationNo varchar(12) PRIMARY key,
        cityCode varchar(10),
        townCode varchar(12),
        DBupdateTime int
        );
        """
    )
    postgres_manager.conn.commit()
    cur.close()
    postgres_manager.closeConnection()


def saveRainWarningData():
    postgres_manager = PostgresBaseManager()
    cur = postgres_manager.conn.cursor()
    rain_warn_api = "https://fhy.wra.gov.tw/WraApi/v1/Rain/Warning"
    rain_warn_info = requests.get(rain_warn_api).json()
    for info in rain_warn_info:
        print(info)
        stationNo = info["StationNo"]
        townCode = info["TownCode"]
        APIupdateTime = dateToStamp(info["Time"])
        DBupdateTime = dateToStamp(str(datetime.now()))
        warningLevel = info["WarningLevel"]
        cur.execute(
            f"INSERT INTO Rain_Warning (stationNo, townCode, APIupdateTime, DBupdateTime, warningLevel) VALUES ('{stationNo}', '{townCode}', {APIupdateTime}, {DBupdateTime}, {warningLevel});")
    postgres_manager.conn.commit()
    cur.close()
    postgres_manager.closeConnection()


def saveWaterWarningData():
    postgres_manager = PostgresBaseManager()
    cur = postgres_manager.conn.cursor()
    water_warn_api = "https://fhy.wra.gov.tw/WraApi/v1/Water/Warning"
    water_warn_info = requests.get(water_warn_api).json()
    for info in water_warn_info:
        print(info)
        stationNo = info["StationNo"]
        townCode = info["TownCode"]
        APIupdateTime = dateToStamp(info["Time"])
        DBupdateTime = dateToStamp(str(datetime.now()))
        warningLevel = info["WarningLevel"]
        cur.execute(
            f"INSERT INTO Water_Warning (stationNo, townCode, APIupdateTime, DBupdateTime, warningLevel) VALUES ('{stationNo}', '{townCode}', {APIupdateTime}, {DBupdateTime}, {warningLevel});")
    postgres_manager.conn.commit()
    cur.close()
    postgres_manager.closeConnection()


def saveReservoirWarningData():
    postgres_manager = PostgresBaseManager()
    cur = postgres_manager.conn.cursor()
    reservoir_warn_api = "https://fhy.wra.gov.tw/WraApi/v1/Reservoir/Warning"
    reservoir_warn_info = requests.get(reservoir_warn_api).json()
    for info in reservoir_warn_info:
        print(info)
        stationNo = info["StationNo"]
        townCode = info["TownCode"]
        APIupdateTime = dateToStamp(info["Time"])
        DBupdateTime = dateToStamp(str(datetime.now()))
        nextSpillTime = dateToStamp(info["NextSpillTime"])
        cur.execute(
            f"INSERT INTO Reservoir_Warning (stationNo, townCode, APIupdateTime, DBupdateTime, NextSpillTime) VALUES ('{stationNo}', '{townCode}', {APIupdateTime}, {DBupdateTime}, {nextSpillTime});")
    postgres_manager.conn.commit()
    cur.close()
    postgres_manager.closeConnection()


def saveRainStation():
    postgres_manager = PostgresBaseManager()
    cur = postgres_manager.conn.cursor()
    rain_station_api = "https://fhy.wra.gov.tw/WraApi/v1/Rain/Station"
    rain_station_info = requests.get(rain_station_api).json()
    values = []
    for info in rain_station_info:
        print(info)
        stationNo = info["StationNo"]
        latitude = info["Latitude"]
        longitude = info["Longitude"]
        DBupdateTime = dateToStamp(str(datetime.now()))
        values.append((stationNo, latitude, longitude, DBupdateTime))
        # cur.execute(
        #     f"INSERT INTO Rain_Station (stationNo, Latitude, Longitude, DBupdateTime) VALUES ('{stationNo}', {latitude}, {longitude}, {DBupdateTime});")
    sql = "INSERT INTO Rain_Station (stationNo, Latitude, Longitude, DBupdateTime) VALUES (%s, %s, %s, %s)"
    cur.executemany(sql, values)
    postgres_manager.conn.commit()
    cur.close()
    postgres_manager.closeConnection()


def saveWaterStation():
    postgres_manager = PostgresBaseManager()
    cur = postgres_manager.conn.cursor()
    water_station_api = "https://fhy.wra.gov.tw/WraApi/v1/Water/Station"
    water_station_info = requests.get(water_station_api).json()
    rows = []
    for info in water_station_info:
        print(info)
        try:
            stationNo = info["StationNo"]
            latitude = info["Latitude"]
            longitude = info["Longitude"]
            DBupdateTime = dateToStamp(str(datetime.now()))
            rows.append((stationNo, latitude, longitude, DBupdateTime))
        except:
            continue
    sql = "INSERT INTO Water_Station (stationNo, Latitude, Longitude, DBupdateTime) VALUES %s"
    extras.execute_values(cur, sql, rows)
    postgres_manager.conn.commit()
    cur.close()
    postgres_manager.closeConnection()


def saveReservoirStation():
    postgres_manager = PostgresBaseManager()
    cur = postgres_manager.conn.cursor()
    reservoir_station_api = "https://fhy.wra.gov.tw/WraApi/v1/Reservoir/Station"
    reservoir_station_info = requests.get(reservoir_station_api).json()
    rows = []
    for info in reservoir_station_info:
        print(info)
        try:
            stationNo = info["StationNo"]
            latitude = info["Latitude"]
            longitude = info["Longitude"]
            DBupdateTime = dateToStamp(str(datetime.now()))
            rows.append((stationNo, latitude, longitude, DBupdateTime))
        except:
            continue
    sql = "INSERT INTO Reservoir_Station (stationNo, Latitude, Longitude, DBupdateTime) VALUES %s"
    extras.execute_values(cur, sql, rows)
    postgres_manager.conn.commit()
    cur.close()
    postgres_manager.closeConnection()


def truncateTable(table):
    postgres_manager = PostgresBaseManager()
    cur = postgres_manager.conn.cursor()
    cur.execute(f" TRUNCATE TABLE {table}")
    postgres_manager.conn.commit()
    cur.close()
    postgres_manager.closeConnection()


if __name__ == "__main__":
    saveReservoirStation()
