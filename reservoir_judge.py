from datetime import datetime
from db_operator.base_manager import PostgresBaseManager
from db_operator.save_from_wra import save_fake_to_reservoir_warning


def opaeration(sql):
    postgres_manager = PostgresBaseManager()
    cur = postgres_manager.conn.cursor()
    results = []
    try:
        cur.execute(sql)
        # Retrieve all rows from the PostgreSQL table
        results = cur.fetchall()
        postgres_manager.conn.commit()
    except Exception as e:
        print("Read failed.")
        print(e)
    finally:
        cur.close()
        return results

# # 加入新測資
# save_fake_to_reservoir_warning()


def reservoir_judge(user_town_code):
    read_re_warn_sql = "SELECT * FROM Reservoir_Warning"
    # staionNo, townCode, APItime, DBtime, nextSpillTime, status ['0: 預計放水', '1: 放水中', '-1: 未放水']
    datas = opaeration(read_re_warn_sql)
    result = []
    for data in datas:
        nextSpillTime = datetime.fromtimestamp(data[4])
        cur_time = datetime.now()
        delta_time = (nextSpillTime - cur_time).seconds
        status = data[5]
        # check time first to reduce times to read DB
        # in case if status doesn't fit time, all the cases in status "1" would be reported
        if delta_time <= 108000 or status[0] == "1":
            stationNo = data[0]
            get_affect_sql = f"SELECT townCode FROM Reservoir_AffectedArea WHERE stationNo='{stationNo}'"
            # [(townCode1), (townCode2),...]
            affect_area = opaeration(get_affect_sql)
            for i in affect_area:
                # if user in the affected area and nextSpillTime - cur_time <= 3hr(10800sec)
                if user_town_code == i[0]:
                    get_reservoir_name_sql = f"SELECT stationName FROM Reservoir_Station WHERE stationNo='{stationNo}'"
                    # [(stationName)] => String
                    reservoir_name = opaeration(get_reservoir_name_sql)[0][0]
                    msg = {"reservoir_name": reservoir_name,
                           "nextSpillTime": nextSpillTime, "status": status}
                    result.append(msg)

    # [{'reservoir_name': string, 'nextSpillTime': datetime.datetime(object)), 'status': string}, ...]
    return result


if __name__ == "__main__":
    # # fit 1 case
    # user_town_code = "6700100"

    # fit 2 case
    user_town_code = "6700600"
    print(reservoir_judge(user_town_code))
