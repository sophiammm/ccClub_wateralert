from db_operator.read_from_db import read
from datetime import datetime
import sys
sys.path.append("../")


def reservoir_judge(user_town_code):
    read_re_warn_sql = "SELECT * FROM Reservoir_Warning"
    # staionNo, townCode, APItime, DBtime, nextSpillTime, status ['0: 預計放水', '1: 放水中', '-1: 未放水']
    datas = read(read_re_warn_sql)
    result = []
    for data in datas:
        status = data[5]
        # has nextSpillTime
        try:
            nextSpillTime = datetime.fromtimestamp(data[4])
            cur_time = datetime.now()
            delta_time = (nextSpillTime - cur_time).seconds
            # check time first to reduce times to read DB
            # in case if status doesn't fit time, all the cases in status "1" would be reported
            if delta_time <= 108000 or status[0] == "1":
                stationNo = data[0]
                get_affect_sql = f"SELECT townCode FROM Reservoir_AffectedArea WHERE stationNo='{stationNo}'"
                affect_area = read(get_affect_sql)
            nextSpillTime = nextSpillTime.strftime("%Y-%m-%d %H:%M")
        # no nextSpillTime
        except:
            if status[0] == "1":
                stationNo = data[0]
                get_affect_sql = f"SELECT townCode FROM Reservoir_AffectedArea WHERE stationNo='{stationNo}'"
                affect_area = read(get_affect_sql)
            nextSpillTime = "目前無資料"
        finally:
            # [(townCode1), (townCode2),...]
            status = status.split(":")[1]
            for i in affect_area:
                # if user in the affected area and nextSpillTime - cur_time <= 3hr(10800sec)
                if user_town_code == i[0]:

                    get_reservoir_name_sql = f"SELECT stationName FROM Reservoir_Station WHERE stationNo='{stationNo}'"
                    # [(stationName)] => String
                    reservoir_name = read(get_reservoir_name_sql)[0][0]
                    msg = {"reservoir_name": reservoir_name,
                           "nextSpillTime": nextSpillTime, "status": status}
                    result.append(msg)

    # [{'reservoir_name': string, 'nextSpillTime': string, 'status': string}, ...]
    return result


if __name__ == "__main__":
    # # fit 1 case
    user_town_code = "6700100"

    # fit 2 case
    # user_town_code = "6700600"
    print(reservoir_judge(user_town_code))
