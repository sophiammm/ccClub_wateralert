from db_operator.read_from_db import read_town_code


def message_text(get_message):
    get_message = get_message.replace('台', '臺')  # 先將「台」轉換成「臺」，因為Database一律用「臺」
    if len(get_message) < 5 or len(get_message) > 7:  # 行政區總共5到7個字而已
        result = ""
    elif '鄉' not in get_message and '鎮' not in get_message and '市' not in get_message and '區' not in get_message:
        result = ""
    elif get_message[2] != '縣' and get_message[2] != '市':  # 第3個字不是縣也不是市
        result = ""
    elif get_message[-1] != '鄉' and get_message[-1] != '鎮' and get_message[-1] != '市' and get_message[-1] != '區':
        result = ""
    else:
        city = get_message[:3]
        town = get_message[3:]
        try:  # 若在Database找不到User輸入的內容，就跑except
            result = read_town_code(city, town)[0][0]
        except:
            result = ""

    return result  # return user_town_code


def message_location(get_message):
    get_message = get_message.replace('台', '臺')  # 先將「台」轉換成「臺」，因為Database一律用「臺」
    try:  # 若在Database找不到User輸入的內容，就跑except
        index = get_message.find('灣')
        city = get_message[index+1:index+4]  # 縣市級都只有三個字，e.g. 桃園市
        town = []
        i = index+4  # 從縣市後第一個字開始抓取
        while get_message[i] != '鄉' and get_message[i] != '鎮' and get_message[i] != '市' and get_message[i] != '區':  # 遇上這四個字，就取消索引的抓取
            town.append(get_message[i])
            i += 1
        town.append(get_message[i])  # 補上'鄉' or '鎮' or '市' or '區'
        # 暫時將town轉成str，以利進行下一列的if判斷
        temp_convert_to_str = "".join(town)
        if temp_convert_to_str == '前鎮' or temp_convert_to_str == '左鎮' or temp_convert_to_str == '平鎮' or temp_convert_to_str == '新市':  # 這四個town的第二字就是'鄉鎮市區'，因此還需要再補後一個字
            town.append(get_message[i+1])  # 補上'鄉' or '鎮' or '市' or '區'
        town = "".join(town)  # 正式將town轉成str
        result = read_town_code(city, town)[0][0]
    except:
        result = ""

    return result  # return user_town_code
