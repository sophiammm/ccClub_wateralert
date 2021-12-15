import psycopg2
import os
from dotenv import load_dotenv


# basic operation of SQL
class PostgresBaseManager:

    def __init__(self):
        # 讀取環境變數
        load_dotenv(dotenv_path='.env', override=True)
        self.database = os.getenv("DATABASE")
        self.user = os.getenv("USER")
        self.password = os.getenv("PASSWORD")
        self.host = os.getenv("HOST")
        self.port = os.getenv("PORT")
        self.conn = self.connectServer()

    def connectServer(self):
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

    def closeConnection(self):
        """
        :return: 關閉資料庫連線使用
        """
        self.conn.close()

    def testServer(self):
        """
        :return: 測試是否可以連線到 Heroku Postgres SQL
        """
        cur = self.conn.cursor()
        cur.execute('SELECT VERSION()')
        results = cur.fetchall()
        print("Database version : {0} ".format(results))
        self.conn.commit()
        cur.close()

    # 待改寫
    def testInsert(self, arg):
        """
        :retrun: 測試新增資料進指定table
        """
        para = (arg["code"], arg["ch"], arg["en"])
        cur = self.conn.cursor()
        try:
            cur.execute(
                'INSERT INTO basic (CityCode, CityName_Ch, CityName_En) VALUES (%s, %s, %s)', para)
            self.conn.commit()
            print("Data has been saved successfully.")
        except:
            print("Data already exists. Cannot been saved again. ")
        finally:
            cur.close()

    def testUpdate(self, target, correct, condition):
        """
        :return: 測試更新資料進指定table
        """
        cur = self.conn.cursor()
        try:
            # 另一種格式化寫法
            # 需要注意SQL語法, SQL語法裡有''的地方還是要加上去
            cur.execute(
                f"UPDATE basic SET {target} = '{correct}' WHERE {condition[0]} = '{condition[1]}'")
            self.conn.commit()
            print("Data has been updated successfully.")
        # 若有Error, print出Error資訊的寫法, 方便知道哪裡出錯
        except Exception as e:
            print("Update failed.")
            print(e)
        finally:
            cur.close()

    def testRead(self, table):
        """
        :return: 測試指定table讀取資料
        暫時不弄成以表格呈現
        """
        cur = self.conn.cursor()
        try:
            cur.execute(
                f"SELECT * FROM {table}")
            # Retrieve all rows from the PostgreSQL table
            results = cur.fetchall()
            self.conn.commit()
            # Print each row and it's columns values
            for row in results:
                print(f"CityCode: {row[0]}")
                print(f"CityName_Ch: {row[1]}")
                print(f"CityName_En: {row[2]}", "\n")

        # 若有Error, print出Error資訊的寫法, 方便知道哪裡出錯
        except Exception as e:
            print("Read failed.")
            print(e)
        finally:
            cur.close()

    def testDelete(self, table, condition):
        """
        :return: 測試指定table讀取資料
        暫時不弄成以表格呈現
        """
        cur = self.conn.cursor()
        try:
            cur.execute(
                f"DELETE FROM {table} WHERE {condition[0]} = '{condition[1]}'")
            self.conn.commit()
            print("Data has been deleted successfully.")

        # 若有Error, print出Error資訊的寫法, 方便知道哪裡出錯
        except Exception as e:
            print("Delete failed.")
            print(e)
        finally:
            cur.close()


# CRUD operation of SQL
# Create Read Update Delete
