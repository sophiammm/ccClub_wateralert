from db_operator.read_from_db import check_warn, read_town_code
# https://github.com/line/line-bot-sdk-python
from linebot.models import TextSendMessage

def input_text(get_message): # User打字輸入行政區
    get_message = get_message.replace('台', '臺')  # 先將「台」轉換成「臺」，因為Database一律用「臺」

    correct_input = TextSendMessage(
        text="⚠️請更正欲查詢水情之行政區的錯字或遺漏字，並符合5至7個字。\n例如: 嘉義縣阿里山鄉、臺東縣成功鎮、南投縣南投市、臺中市西區。\n\n⚠️或是在介面左下方「＋」選擇位置資訊，並根據您的所在位置或是指定位置發送給我。")

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
                        msg += f"{warn[target]}\n"
                    except:
                        break
                return msg

            re_msg = warn_msg(re_warns, 2)
            rain_msg = warn_msg(rain_warns, 0)
            water_msg = warn_msg(water_warns, 0)

            if water_msg != "" or re_msg != "" or rain_msg != "":
                water_condition = f"water:{water_msg}\n\nrain:{rain_msg}\n\nreservoir:{re_msg}"
            else:
                water_condition = "指定地區安全"

            output = TextSendMessage(
                text=f"您輸入的是：{get_message}\n此區域的水情狀況⬇\n{water_condition}")
            reply = output
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
        address_town = address_town.replace(
            '台', '臺')  # 將「台」轉換成「臺」，因為Database一律用「臺」

        reply = TextSendMessage(
            text=f'您選取的位置為:\n{get_message}\n\ncity:\n{address_city}\n\ntown:\n{address_town}\n\n緯度:\n{latitude}\n\n經度:\n{longitude}')
    except:
        reply = TextSendMessage(text='請重新發送位置資訊。')
    return(reply)