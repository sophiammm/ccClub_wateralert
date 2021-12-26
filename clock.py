import os
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime
from flask_mail import Mail, Message
from db_operator.update import update_rain_warning, update_water_warning, update_reservoir_warning
from db_operator.read_from_db import read_one, read, read_town_code
from reply import input_location
from gps_address import gps_to_address
from app import create_app

app = create_app()

mail_settings = {
    "MAIL_SERVER": "smtp.gmail.com",
    "MAIL_PORT": 587,
    "MAIL_USERNAME": os.getenv("MAIL_USERNAME"),
    "MAIL_PASSWORD": os.getenv("MAIL_PASSWORD"),
    "MAIL_USE_TLS": True,
    "MAIL_USE_SSL": False
}
app.config.update(mail_settings)
mail = Mail(app)

sched = BlockingScheduler()


def get_usr():
    sql = f"SELECT ownerID, latitude, longitude from UsrLocation;"
    usr_list = read(sql)
    return usr_list


def send_warn(usr_email, info):
    msg = Message('水情警報!!', sender=os.getenv("MAIL_USERNAME"),
                  recipients=[usr_email])
    msg.body = f"{info}"
    try:
        mail.send(msg)
        return "Sent"
    except Exception as e:
        print(e)
        return "Error"


@sched.scheduled_job('interval', id='save_warn', minutes=10, misfire_grace_time=120)
def save_warn_from_wra():
    print('task executed at ' + str(datetime.now()))
    # try catch real data
    update_rain_warning()
    update_water_warning()
    update_reservoir_warning()


@sched.scheduled_job('interval', id='send_warn', minutes=10, jitter=120, misfire_grace_time=180)
def send_mail():
    with app.app_context():
        usr_list = get_usr()
        for usr in usr_list:
            lat = usr[1]
            lon = usr[2]
            usr_address = gps_to_address((lat, lon))
            usr_town_code = read_town_code(usr_address[:3], usr_address[3:])
            water_condition = input_location(usr_town_code, lat, lon)
            if water_condition["water"] == '無警戒。' and water_condition["rain"] == '無警戒。' and water_condition["reservoir"] == '無警戒。':
                continue
            else:
                sql = f"SELECT usrname, email from Usr WHERE id={usr[0]};"
                usr_detail = read_one(sql)
                url = "https://wateralert.herokuapp.com/"
                info = f"您的登記地區:\n{usr_address}\n目前有發布水情警報\n請提高警覺\n警報細節如下⬇\n\n河川: \n{water_condition['water']}\n\n雨勢: \n{water_condition['rain']}\n\n水庫: \n{water_condition['reservoir']}\n若需更新位置資訊\n請至Water Alert網站: {url}\n如欲取消警示通知\n請將帳號登出"
                usr_mail = usr_detail["email"]
                send_warn(usr_mail, info)


sched.start()
