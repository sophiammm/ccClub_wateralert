import requests
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_apscheduler import APScheduler
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


# set configuration values
class Config:
    SCHEDULER_API_ENABLED = True
    SCHEDULER_TIMEZONE = "Asia/Taipei"  # <========== 設置時區, 時區不一致可能會導致任務時間出錯


# init server
app = Flask(__name__)
app.config.from_object(Config())
# 測試階段先開啟DEBUG, 正式運行要關掉
app.config['DEBUG'] = True


# functions to get data from wra api
def cityNameToCodeAndEn(cityCN):
    url = f"https://fhy.wra.gov.tw/WraApi/v1/Basic/City?$filter=CityName_Ch%20eq%20'{cityCN}'"
    re = requests.get(url).json()
    return {"code": re[0]["CityCode"], "en": re[0]["CityName_En"], "ch": re[0]["CityName_Ch"]}


def townNameToCode(cityEn, town):
    url = f"https://fhy.wra.gov.tw/WraApi/v1/Basic/{cityEn}/Town?$filter=TownName%20eq%20'{town}'"
    re = requests.get(url).json()
    try:
        result = re[0]["TownCode"]
    except:
        result = "No Data"
    return result


def getWaterWarning(cityCode):
    url = f"https://fhy.wra.gov.tw/WraApi/v1/Water/Warning?$filter=CityCode%20eq%20'{cityCode}'"
    re = requests.get(url).json()
    if re != []:
        result = re
    else:
        result = "No warning."
    return result


def getWaterStationTown(town=""):
    if town == "":
        url = "https://fhy.wra.gov.tw/WraApi/v1/Water/Station"
    else:
        url = f"https://fhy.wra.gov.tw/WraApi/v1/Water/Station?$filter=contains(Address%2C'{town}')"
    re = requests.get(url).json()
    return re


def getWaterStationCity(CityCode=""):
    if CityCode == "":
        url = "https://fhy.wra.gov.tw/WraApi/v1/Water/Station"
    else:
        url = f"https://fhy.wra.gov.tw/WraApi/v1/Water/Station?$filter=CityCode%20eq%20'{CityCode}'"
    re = requests.get(url).json()
    return re


def getWaterRealtime(StationNo):
    re = requests.get(
        "https://fhy.wra.gov.tw/WraApi/v1/Water/RealTimeInfo").json()
    return re


# initial route
@ app.route('/', methods=['GET'])
def index():
    return render_template("index.html")


# search route
@ app.route('/search', methods=['GET'])
def search_get():
    return render_template("search.html")


@ app.route("/result", methods=['POST'])
def search_request():
    if request.method == 'POST':
        city = request.values["city"]
        citycode = cityNameToCodeAndEn(city)["code"]
        water_stations = getWaterStationCity(citycode)
        return render_template("result.html", water_stations=water_stations)


def showWarn():
    # Get data from WRA API test
    city = cityNameToCodeAndEn("新北市")
    cityCode = city["code"]
    cityEn = city["en"]
    town = "汐止區"
    print(getWaterWarning(cityCode))
    print(getWaterStationTown(town))


if __name__ == "__main__":

    # # initialize scheduler
    # scheduler = APScheduler()

    # # Add task
    # @scheduler.task('interval', id='do_job_1', seconds=5, misfire_grace_time=900)
    # def job1():
    #     print('Job 1 executed')
    #     showWarn()

    # # if you don't wanna use a config, you can set options here:
    # # scheduler.api_enabled = True
    # scheduler.init_app(app)

    # scheduler.start()

    # # In debug mode, Flask's reloader will load the flask app twice
    # app.run(use_reloader=False)

    # DB測試
    # 連線以及執行DB Manager
    postgres_manager = PostgresBaseManager()

    # # 測試將API資料存進DB
    # arg = cityNameToCodeAndEn(input("城市名:"))
    # print(arg)
    # postgres_manager.testInsert(arg)

    # # 測試UPDATE
    # target = 'CityName_Ch'
    # correct = '宜蘭縣'
    # condition = ['CityCode', '10002']
    # postgres_manager.testUpdate(target, correct, condition)

    # # 測試READ
    # table = "basic"
    # postgres_manager.testRead(table)

    # 測試DELETE
    table = "basic"
    condition = ['CityCode', '10002']
    postgres_manager.testDelete(table, condition)

    # 中斷DB連線
    postgres_manager.closeConnection()
