from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from geopy.exc import GeocoderTimedOut
import time


geolocator = Nominatim(user_agent="waterAlert")


def address_to_gps(address, attempt=1, max_attempts=40):
    # country_codes限制搜尋範圍
    try:
        # set timeout避免 timeout error
        # 版權 https://www.openstreetmap.org/copyright/zh-TW
        location = geolocator.geocode(address, country_codes="TW", timeout=10)
        if location != None:
            lat = location.latitude
            lon = location.longitude
            return lat, lon
        else:
            return
    except GeocoderTimedOut:
        if attempt <= max_attempts:
            time.sleep(2)
            return address_to_gps(address, attempt=attempt+1)
        raise


def gps_to_address(mark):
    location = geolocator.reverse(f"{mark[0]}, {mark[1]}", ).raw["address"]
    try:
        # 台北新北
        if location["state"] != "臺灣省":
            city = location["state"]
        # 台灣省下縣市
        else:
            try:
                city = location["city"]
            except:
                city = location["county"]
    except:
        # 其他直轄市
        city = location["city"]
    # 有些suburb是區, 有些是里, 有town先取town
    try:
        town = location["town"]
    except:
        town = location["suburb"]

    return city + town


def in_range(mark1, mark2, limit):
    distance = geodesic(mark1, mark2).km
    if distance > limit:
        return False
    else:
        return True


if __name__ == "__main__":
    print(address_to_gps("新北市"))
