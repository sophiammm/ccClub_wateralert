from db_operator.base_manager import PostgresBaseManager


def read_table(table):
    postgres_manager = PostgresBaseManager()
    cur = postgres_manager.conn.cursor()
    results = []
    try:
        cur.execute(
            f"SELECT * FROM {table}")
        # Retrieve all rows from the PostgreSQL table
        results = cur.fetchall()
        postgres_manager.conn.commit()
    except Exception as e:
        print("Read failed.")
        print(e)
    finally:
        cur.close()
        return results


# for web
def read_city():
    postgres_manager = PostgresBaseManager()
    cur = postgres_manager.conn.cursor()
    results = []
    try:
        cur.execute(
            "SELECT DISTINCT cityID, cityName FROM City_Town;")
        # Retrieve all rows from the PostgreSQL table
        results = cur.fetchall()
        postgres_manager.conn.commit()
    except Exception as e:
        print("Read failed.")
        print(e)
    finally:
        cur.close()
        return results


def read_town_by_city(city):
    postgres_manager = PostgresBaseManager()
    cur = postgres_manager.conn.cursor()
    results = []
    try:
        cur.execute(
            f"SELECT townName FROM City_Town WHERE cityName='{city}';")
        # Retrieve all rows from the PostgreSQL table
        results = cur.fetchall()
        postgres_manager.conn.commit()
    except Exception as e:
        print("Read failed.")
        print(e)
    finally:
        cur.close()
        return results


# linebot
def read_townID(city, town):
    postgres_manager = PostgresBaseManager()
    cur = postgres_manager.conn.cursor()
    results = []
    try:
        cur.execute(
            f"SELECT townID FROM City_Town WHERE cityName='{city}' AND townName='{town}'")
        # Retrieve all rows from the PostgreSQL table
        results = cur.fetchall()
        postgres_manager.conn.commit()
    except Exception as e:
        print("Read failed.")
        print(e)
    finally:
        cur.close()
        return results


def check_warn(town_id):
    postgres_manager = PostgresBaseManager()
    cur = postgres_manager.conn.cursor()
    rain_results = []
    water_results = []
    try:
        cur.execute(
            f"SELECT stationNo FROM Rain_Warning WHERE townCode='{town_id}';")
        rain_results = cur.fetchall()
        cur.execute(
            f"SELECT stationNo FROM Water_Warning WHERE townCode='{town_id}';")
        water_results = cur.fetchall()
        cur.execute(
            f"SELECT stationNo FROM Reservoir_Warning WHERE townCode='{town_id}';")
        reservoir_results = cur.fetchall()

        postgres_manager.conn.commit()
    except Exception as e:
        print("Read failed.")
        print(e)
    finally:
        cur.close()
        return {"water": water_results, "rain": rain_results, "reservoir": reservoir_results}
