from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime
from db_operator.update import update_rain_warning, update_water_warning, update_reservoir_warning

sched = BlockingScheduler()


@sched.scheduled_job('interval', id='save_warn', minutes=10)
def save_warn_from_wra():
    print('task executed at ' + str(datetime.now()))
    update_rain_warning()
    update_water_warning()
    update_reservoir_warning()


sched.start()
