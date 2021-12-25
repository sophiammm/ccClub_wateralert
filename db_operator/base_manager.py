import psycopg2
import os
from dotenv import load_dotenv


# basic operation of SQL
class PostgresBaseManager:

    # # for local run
    # def __init__(self):
    #     # 讀取環境變數
    #     load_dotenv(dotenv_path='.env', override=True)
    #     self.database = os.getenv("DATABASE")
    #     self.user = os.getenv("USER")
    #     self.password = os.getenv("PASSWORD")
    #     self.host = os.getenv("HOST")
    #     self.port = os.getenv("PORT")
    #     self.conn = self.connect_server()

    # for server run
    def __init__(self):
        # 讀取環境變數
        load_dotenv(dotenv_path='.env', override=True)
        self.database = os.getenv("DATABASE_sql")
        self.user = os.getenv("USER_sql")
        self.password = os.getenv("PASSWORD_sql")
        self.host = os.getenv("HOST_sql")
        self.port = os.getenv("PORT_sql")
        self.conn = self.connect_server()

    def connect_server(self):
        """
        :return: 連接 Heroku Postgres SQL 認證用
        """
        conn = psycopg2.connect(
            database=self.database,
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port)
        return conn

    def close_connection(self):
        """
        :return: 關閉資料庫連線使用
        """
        self.conn.close()

    def test_server(self):
        """
        :return: 測試是否可以連線到 Heroku Postgres SQL
        """
        cur = self.conn.cursor()
        cur.execute('SELECT VERSION()')
        results = cur.fetchall()
        print("Database version : {0} ".format(results))
        self.conn.commit()
        cur.close()


# for test
if __name__ == "__main__":
    postgres_manager = PostgresBaseManager()
    postgres_manager.test_server()
    postgres_manager.close_connection()
