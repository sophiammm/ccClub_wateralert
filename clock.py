from apscheduler.schedulers.blocking import BlockingScheduler
# from datetime import datetime
# import sys
# from db_operator.update_from_wra import update_rain_warning, update_water_warning, update_reservoir_warning

sched = BlockingScheduler()


@sched.scheduled_job('interval', id='save_warn', minutes=1)
def test():
    print('This job if for test.')


# @sched.scheduled_job('interval', id='save_warn', minutes=10)
# def save_warn_from_wra():
#     print('task executed at ' + str(datetime.now()))
#     sys.stdout.flush()
#     update_rain_warning()
#     update_water_warning()
#     update_reservoir_warning()


sched.start()
