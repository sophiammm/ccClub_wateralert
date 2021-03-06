from judgement.initial_check import message_text, message_location
from judgement.water_judge import water_judge_by_town, water_judge_by_location
from judgement.rain_judge import rain_judge_by_town, rain_judge_by_location
from judgement.reservoir_judge import reservoir_judge


def input_text(user_town_code):  # User打字輸入行政區
    waterLevel_remark = {1: '河川水位預計未來2小時到達計畫洪水位(或堤頂)時之水位。',
                         2: '河川水位預計未來5小時到達計畫洪水位(或堤頂)時之水位。',
                         3: '河川水位預計未來2小時到達高灘地之水位。'
                         }
    water_msg = []
    water_results = water_judge_by_town(user_town_code)
    if water_results == []:
        water_msg = '無警戒。'
    else:
        for water_result in water_results:
            water_msg.append(
                f"{water_result['basinName']}有{water_result['warningLevel']}級警戒。\n{waterLevel_remark[water_result['warningLevel']]}")
        water_msg = "\n".join(water_msg)  # list轉str，並換行。

    rainLevel_remark = {1: '發布淹水警戒之鄉(鎮、市、區)如持續降雨，其轄內易淹水村里有70%機率已開始積淹水。',
                        2: '發布淹水警戒之鄉(鎮、市、區)如持續降雨，其轄內易淹水村里有70%機率三小時內開始積淹水。'
                        }
    rain_msg = ""
    rain_result = rain_judge_by_town(user_town_code)[0]
    # e.g. 會取[0]是因為return出來是[{'warningLevel': 1}]，而rain的list只會有一個字典，所以無需像water使用for取出每個字典。
    rain_msg = f"{rain_result['warningLevel']}級警戒。"
    if rain_msg == "0級警戒。":
        rain_msg = '無警戒。'
    else:
        rain_msg = f"{rain_result['warningLevel']}級警戒。\n{rainLevel_remark[rain_result['warningLevel']]}"

    reservoir_msg = []
    reservoir_results = reservoir_judge(user_town_code)
    if reservoir_results == []:
        reservoir_msg = '無警戒。'
    else:
        for reservoir_result in reservoir_results:
            reservoir_msg.append(
                f"{reservoir_result['reservoir_name']}的放水狀態為: {reservoir_result['status']}。\n預計放水時間為: {reservoir_result['nextSpillTime']}。")
        reservoir_msg = "\n".join(reservoir_msg)  # list轉str，並換行。

    water_condition = {'water': water_msg,
                       'rain': rain_msg, 'reservoir': reservoir_msg}

    return water_condition


def input_location(user_town_code, latitude, longitude):  # User發送位置資訊
    waterLevel_remark = {1: '河川水位預計未來2小時到達計畫洪水位(或堤頂)時之水位。',
                         2: '河川水位預計未來5小時到達計畫洪水位(或堤頂)時之水位。',
                         3: '河川水位預計未來2小時到達高灘地之水位。'
                         }
    water_msg = []
    water_results = water_judge_by_location(latitude, longitude)
    if water_results == []:
        water_msg = '無警戒。'
    else:
        for water_result in water_results:
            water_msg.append(
                f"{water_result['basinName']}有{water_result['warningLevel']}級警戒。\n{waterLevel_remark[water_result['warningLevel']]}")
        water_msg = "\n".join(water_msg)  # list轉str，並換行。

    rainLevel_remark = {1: '發布淹水警戒之鄉(鎮、市、區)如持續降雨，其轄內易淹水村里有70%機率已開始積淹水。',
                        2: '發布淹水警戒之鄉(鎮、市、區)如持續降雨，其轄內易淹水村里有70%機率三小時內開始積淹水。'
                        }
    rain_msg = ""
    rain_result = rain_judge_by_location(latitude, longitude)[0]
    # e.g. 會取[0]是因為return出來是[{'warningLevel': 1}]，而rain的list只會有一個字典，所以無需像water使用for取出每個字典。
    rain_msg = f"{rain_result['warningLevel']}級警戒。"
    if rain_msg == "0級警戒。":
        rain_msg = '無警戒。'
    else:
        rain_msg = f"{rain_result['warningLevel']}級警戒。\n{rainLevel_remark[rain_result['warningLevel']]}"

    reservoir_msg = []
    reservoir_results = reservoir_judge(user_town_code)
    if reservoir_results == []:
        reservoir_msg = '無警戒。'
    else:
        for reservoir_result in reservoir_results:
            reservoir_msg.append(
                f"{reservoir_result['reservoir_name']}的放水狀態為: {reservoir_result['status']}。\n預計放水時間為: {reservoir_result['nextSpillTime']}。")
        reservoir_msg = "\n".join(reservoir_msg)  # list轉str，並換行。

    water_condition = {'water': water_msg,
                       'rain': rain_msg, 'reservoir': reservoir_msg}

    return water_condition
