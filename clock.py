import os
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime
from flask_mail import Mail, Message
from db_operator.update import update_rain_warning, update_water_warning, update_reservoir_warning
from db_operator.read_from_db import read_one
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


def send_warn(usr_email, info):
    msg = Message('Water Alert', sender=os.getenv("MAIL_USERNAME"),
                  recipients=[usr_email])
    msg.body = f"{info}"
    try:
        mail.send(msg)
        return "Sent"
    except Exception as e:
        print(e)
        return "Error"


@sched.scheduled_job('interval', id='save_warn', minutes=10)
def save_warn_from_wra():
    print('task executed at ' + str(datetime.now()))
    update_rain_warning()
    update_water_warning()
    update_reservoir_warning()


# @sched.scheduled_job('interval', id='send_warn', minutes=1)
# def send_mail():
#     with app.app_context():
#         sql = f"SELECT usrname, email from Usr WHERE id=2;"
#         usr_detail = read_one(sql)
#         info = f"Hi {usr_detail['usrname']}"
#         usr_mail = usr_detail["email"]
#         send_warn(usr_mail, info)


sched.start()
