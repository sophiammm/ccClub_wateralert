from db_operator.base_manager import PostgresBaseManager
from psycopg2 import extras


def read(sql):
    postgres_manager = PostgresBaseManager()
    cur = postgres_manager.conn.cursor()
    results = []
    try:
        cur.execute(sql)
        # Retrieve all rows from the PostgreSQL table
        results = cur.fetchall()
        postgres_manager.conn.commit()
    except Exception as e:
        print("Read failed.")
        print(e)
    finally:
        cur.close()
        return results


def read_one(sql):
    postgres_manager = PostgresBaseManager()
    cur = postgres_manager.conn.cursor(cursor_factory=extras.DictCursor)
    results = []
    try:
        cur.execute(sql)
        # Retrieve one row from the PostgreSQL table
        results = cur.fetchone()
        postgres_manager.conn.commit()
    except Exception as e:
        print("Read failed.")
        print(e)
    finally:
        cur.close()
        return results


def read_table(table):
    read_table_sql = f"SELECT * FROM {table}"
    return read(read_table_sql)


# for web
def read_city():
    read_city_sql = "SELECT DISTINCT cityCode, cityName FROM City_Town;"
    return read(read_city_sql)


def read_town_by_city_code(cityCode):
    read_town_by_city_code_sql = f"SELECT townCode, townName FROM City_Town WHERE cityCode='{cityCode}';"
    return read(read_town_by_city_code_sql)


def read_address_by_town_code(townCode):
    read_address_by_town_code_sql = f"SELECT cityName ,townName FROM City_Town WHERE townCode='{townCode}';"
    return read(read_address_by_town_code_sql)

# linebot


def read_town_code(city, town):
    postgres_manager = PostgresBaseManager()
    cur = postgres_manager.conn.cursor()
    results = []
    try:
        cur.execute(
            f"SELECT townCode FROM City_Town WHERE cityName='{city}' AND townName='{town}'")
        # Retrieve all rows from the PostgreSQL table
        results = cur.fetchall()
        postgres_manager.conn.commit()
    except Exception as e:
        print("Read failed.")
        print(e)
    finally:
        cur.close()
        return results


def check_warn(town_code):
    postgres_manager = PostgresBaseManager()
    cur = postgres_manager.conn.cursor()
    rain_results = []
    water_results = []
    reservoir_results = []
    try:
        cur.execute(
            f"SELECT warningLevel FROM Rain_Warning WHERE townCode='{town_code}';")
        rain_results = cur.fetchall()
        cur.execute(
            f"SELECT stationNo, warningLevel FROM Water_Warning WHERE townCode='{town_code}';")
        water_results = cur.fetchall()
        cur.execute(
            f"SELECT stationNo, nextSpillTime, status FROM Reservoir_Warning;")
        reservoir_infos = cur.fetchall()
        reservoir_affects = set()
        for info in reservoir_infos:
            cur.execute(
                f"SELECT townCode FROM Reservoir_AffectedArea WHERE stationNo ='{info[0]}';")
            reservoir_affect = cur.fetchall()
            for area in reservoir_affect:
                reservoir_affects.add(area[0])
        if town_code in reservoir_affects:
            # ????????? ???????????????
            # ???????????? ?????????????????????????????????????????? ????????????????????? ?????????
            # ???????????????????????????water, rain??????
            # ????????????????????????????????????, ?????????????????????User?????????
            reservoir_results = reservoir_infos

        postgres_manager.conn.commit()
    except Exception as e:
        print("Read failed.")
        print(e)
    finally:
        cur.close()
        return {"water": water_results, "rain": rain_results, "reservoir": reservoir_results}


def check_reservoir_name(station_code):
    postgres_manager = PostgresBaseManager()
    cur = postgres_manager.conn.cursor()
    results = []
    try:
        cur.execute(
            f"SELECT stationName FROM Reservoir_Station WHERE stationNo='{station_code}';")
        # Retrieve all rows from the PostgreSQL table
        results = cur.fetchall()
        postgres_manager.conn.commit()
    except Exception as e:
        print("Read failed.")
        print(e)
    finally:
        cur.close()
        return results


def read_water_station(station_code):
    postgres_manager = PostgresBaseManager()
    cur = postgres_manager.conn.cursor()
    results = []
    try:
        cur.execute(
            f"SELECT basinName, latitude, longitude FROM Water_Station WHERE stationNo='{station_code}';")
        # Retrieve all rows from the PostgreSQL table
        results = cur.fetchall()
        postgres_manager.conn.commit()
    except Exception as e:
        print("Read failed.")
        print(e)
    finally:
        cur.close()
        return results
