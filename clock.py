from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime
from db_operator.update import update_rain_warning, update_water_warning, update_reservoir_warning
from db_operator.read_from_db import read_one
from app import send_warn, create_app

app = create_app()

sched = BlockingScheduler()


@sched.scheduled_job('interval', id='save_warn', minutes=10)
def save_warn_from_wra():
    print('task executed at ' + str(datetime.now()))
    update_rain_warning()
    update_water_warning()
    update_reservoir_warning()


# @sched.scheduled_job('interval', id='send_warn', minutes=1)
# def send_mail():
#     with app.app_context():
#         usr_id = 2
#         sql = f"SELECT usrname, email from Usr WHERE id='{usr_id}';"
#         usr_detail = read_one(sql)
#         info = f"Hi {usr_detail['usrname']}"
#         usr_mail = usr_detail["email"]
#         send_warn(usr_mail, info)


sched.start()
