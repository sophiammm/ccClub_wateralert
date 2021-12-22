from db_operator.read_from_db import check_warn, read_town_code, check_water_basinName, check_reservoir_name
# https://github.com/line/line-bot-sdk-python

def input_text(get_message): # User打字輸入行政區
    get_message = get_message.replace('台', '臺')  # 先將「台」轉換成「臺」，因為Database一律用「臺」

    correct_input = "⚠️請檢查欲查詢水情之行政區的錯字或遺漏字，並符合5至7個字。\n例如: 嘉義縣阿里山鄉、臺東縣成功鎮、南投縣南投市、臺中市西區。\n\n⚠️或是在介面左下方「＋」選擇位置資訊，並根據您的所在位置或是指定位置發送給我。"

    if len(get_message) < 5 or len(get_message) > 7:  # 行政區總共5到7個字而已
        reply = correct_input
    elif '鄉' not in get_message and '鎮' not in get_message and '市' not in get_message and '區' not in get_message:
        reply = correct_input
    elif get_message[2] != '縣' and get_message[2] != '市':  # 第3個字不是縣也不是市
        reply = correct_input
    elif get_message[-1] != '鄉' and get_message[-1] != '鎮' and get_message[-1] != '市' and get_message[-1] != '區':
        reply = correct_input
    else:
        address_city = get_message[:3]
        address_town = get_message[3:]
    try: # 若在Database找不到User輸入的內容，就跑except
        town_code = read_town_code(address_city, address_town)[0][0]
        # [(data1), (data2), ],[], []
        warns = check_warn(town_code)
        re_warns = warns["reservoir"]
        rain_warns = warns["rain"]
        water_warns = warns["water"]

        def warn_msg(warns, target):
            msg = ""
            for warn in warns:
                try:
                    msg += f"{warn[target]}"
                except:
                    break
            return msg

        waterLevel_remark = {'1':'河川水位預計未來2小時到達計畫洪水位(或堤頂)時之水位。',
            '2':'河川水位預計未來5小時到達計畫洪水位(或堤頂)時之水位。',
            '3':'河川水位預計未來2小時到達高灘地之水位。'
        }
        rainLevel_remark = {'1':'發布淹水警戒之鄉(鎮、市、區)如持續降雨，其轄內易淹水村里有70%機率已開始積淹水。',
            '2':'發布淹水警戒之鄉(鎮、市、區)如持續降雨，其轄內易淹水村里有70%機率三小時內開始積淹水。'
        }

        water_msg = warn_msg(water_warns, 1) # 0: stationNo, 1: warningLevel
        water_msg_stationNo = warn_msg(water_warns, 0) # 0: stationNo, 1: warningLevel
        rain_msg = warn_msg(rain_warns, 0) # 0: warningLevel
        re_msg = warn_msg(re_warns, 2) # 0: stationNo, 1: nextSpillTime, 2: status
        re_msg_stationNo = warn_msg(re_warns, 0) # 0: stationNo, 1: nextSpillTime, 2: status

        if water_msg != "":
            water_msg = f'{water_msg}級警戒\n{waterLevel_remark[water_msg]}' # 加上級警戒和remark
            water_basinName = f'({check_water_basinName(water_msg_stationNo)[0][0]})' # 得出水庫中文名稱並加上()
        else: 
            water_msg = '無安全警示'
            water_basinName = ""

        if rain_msg != "":
            rain_msg = f'{rain_msg}級警戒\n{rainLevel_remark[rain_msg]}' # 加上級警戒和remark
        else: 
            rain_msg = '無安全警示'

        if re_msg != "":
            re_msg = re_msg[3:]
            re_msg_stationName = f'({check_reservoir_name(re_msg_stationNo)[0][0]})' # 得出水庫中文名稱並加上()
        else:
            re_msg = '無安全警示'
            re_msg_stationName = ""

        water_condition = f"河川{water_basinName}: {water_msg}\n\n雨勢: {rain_msg}\n\n水庫{re_msg_stationName}: {re_msg}"

        reply = f"您輸入的是: {get_message}\n此區域的水情狀況⬇\n{water_condition}"
    
    except:
       reply = correct_input
       
    return(reply)


def input_location(get_message, latitude, longitude): # User發送位置資訊
    get_message = get_message.replace('台', '臺')  # 先將「台」轉換成「臺」，因為Database一律用「臺」
    address_city = get_message[5:8]

    try:
        address_town = []
        i = 8
        while get_message[i] != '鄉' and get_message[i] != '鎮' and get_message[i] != '市' and get_message[i] != '區':  # 遇上這四個字，就取消索引的抓取
            address_town.append(get_message[i])
            i += 1
        address_town.append(get_message[i])  # 補上'鄉' or '鎮' or '市' or '區'
        # 暫時將address_town轉成str，以利進行下一列的if判斷
        temp_convert_to_str = "".join(address_town)
        if temp_convert_to_str == '前鎮' or temp_convert_to_str == '左鎮' or temp_convert_to_str == '平鎮' or temp_convert_to_str == '新市':  # 這四個town的第二字就是'鄉鎮市區'，因此還需要再補後一個字
            address_town.append(get_message[i+1])  # 補上'鄉' or '鎮' or '市' or '區'
        address_town = "".join(address_town)  # 正式將address_town轉成str
        town_code = read_town_code(address_city, address_town)[0][0]
        # [(data1), (data2), ],[], []
        warns = check_warn(town_code)
        re_warns = warns["reservoir"]
        rain_warns = warns["rain"]
        water_warns = warns["water"]

        def warn_msg(warns, target):
            msg = ""
            for warn in warns:
                try:
                    msg += f"{warn[target]}"
                except:
                    break
            return msg

        waterLevel_remark = {'1':'河川水位預計未來2小時到達計畫洪水位(或堤頂)時之水位。',
            '2':'河川水位預計未來5小時到達計畫洪水位(或堤頂)時之水位。',
            '3':'河川水位預計未來2小時到達高灘地之水位。'
        }
        rainLevel_remark = {'1':'發布淹水警戒之鄉(鎮、市、區)如持續降雨，其轄內易淹水村里有70%機率已開始積淹水。',
            '2':'發布淹水警戒之鄉(鎮、市、區)如持續降雨，其轄內易淹水村里有70%機率三小時內開始積淹水。'
        }

        water_msg = warn_msg(water_warns, 1) # 0: stationNo, 1: warningLevel
        water_msg_stationNo = warn_msg(water_warns, 0) # 0: stationNo, 1: warningLevel
        rain_msg = warn_msg(rain_warns, 0) # 0: warningLevel
        re_msg = warn_msg(re_warns, 2) # 0: stationNo, 1: nextSpillTime, 2: status
        re_msg_stationNo = warn_msg(re_warns, 0) # 0: stationNo, 1: nextSpillTime, 2: status

        if water_msg != "":
            water_msg = f'{water_msg}級警戒\n{waterLevel_remark[water_msg]}' # 加上級警戒和remark
            water_basinName = f'({check_water_basinName(water_msg_stationNo)[0][0]})' # 得出水庫中文名稱並加上()
        else: 
            water_msg = '無安全警示'
            water_basinName = ""

        if rain_msg != "":
            rain_msg = f'{rain_msg}級警戒\n{rainLevel_remark[rain_msg]}' # 加上級警戒和remark
        else: 
            rain_msg = '無安全警示'

        if re_msg != "":
            re_msg = re_msg[3:]
            re_msg_stationName = f'({check_reservoir_name(re_msg_stationNo)[0][0]})' # 得出水庫中文名稱並加上()
        else:
            re_msg = '無安全警示'
            re_msg_stationName = ""

        water_condition = f"河川{water_basinName}: {water_msg}\n\n雨勢: {rain_msg}\n\n水庫{re_msg_stationName}: {re_msg}"

        reply = f"您選取的位置是: {get_message}\n緯度: {latitude}\n經度: {longitude}\n\n此區域的水情狀況⬇\n{water_condition}"
    
    except:
        reply = '⚠️請重新發送位置資訊。'
    
    return(reply)
