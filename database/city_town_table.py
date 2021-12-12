import psycopg2
import requests
import os
from dotenv import load_dotenv
import simplejson as json
from psycopg2.extras import RealDictCursor

class PostgresBaseManager:

    def __init__(self):
        # 讀取環境變數
        load_dotenv(dotenv_path='.env', override=True)
        self.database = os.getenv("DATABASE_sql")
        self.user = os.getenv("USER_sql")
        self.password = os.getenv("PASSWORD_sql")
        self.host = os.getenv("HOST_sql")
        self.port = os.getenv("PORT_sql")
        self.conn = self.connectServer()

    def connectServer(self):
        conn = psycopg2.connect(
            database=self.database,
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port)
        return conn

    def closeConnection(self):
        self.conn.close()

    def testServer(self):
        cur = self.conn.cursor()
        cur.execute('SELECT VERSION()')
        results = cur.fetchall()
        print("Database version : {0} ".format(results))
        self.conn.commit()
        cur.close()
    

    def get_json_cursor(self):
        return self.conn.cursor(cursor_factory=RealDictCursor)

    @staticmethod
    def execute_and_fetch(cursor, query):
        cursor.execute(query)
        res = cursor.fetchall()
        cursor.close()
        return res

    def get_json_response(self, query):
        cursor = self.get_json_cursor()
        response = self.execute_and_fetch(cursor, query)
        return json.dumps(response, ensure_ascii=False)

    def get_info(self):
        query = "SELECT * FROM City_Town;"
        return self.get_json_response(query)

postgres_manager = PostgresBaseManager()


# Open a cursor to perform database operations
cur = postgres_manager.conn.cursor()

city_api = "https://fhy.wra.gov.tw/WraApi/v1/Basic/City"
city_info = requests.get(city_api).json()
for info in city_info:
    cityID = info["CityCode"]
    cityName = info["CityName_Ch"]
    cityName_En = info["CityName_En"]
    
    town_api = "https://fhy.wra.gov.tw/WraApi/v1/Basic/{cityName_En}/Town".format(cityName_En = cityName_En)
    town_info = requests.get(town_api).json()
    for info in town_info:
        townID = info["TownCode"]
        townName = info["TownName"]
        
        cur.execute("""
            INSERT INTO City_Town (cityID, cityName, townID, townName)
            VALUES (%s, %s, %s, %s);
            """,
            (f"{cityID}", f"{cityName}", f"{townID}", f"{townName}"))
        postgres_manager.conn.commit()

postgres_manager.get_info()
# tmp = postgres_manager.get_info()
# print(tmp)

# # Execute a query
# cur.execute("SELECT * FROM City_Town")

# # Retrieve query results as list
# records = cur.fetchall()

# # Make the changes to the database persistent
# postgres_manager.conn.commit()

# Close communication with the database
cur.close()
postgres_manager.closeConnection()
