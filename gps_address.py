from geopy.geocoders import Nominatim
from geopy.distance import geodesic

geolocator = Nominatim(user_agent="waterAlert")


def address_to_gps(address):
    # country_codes限制搜尋範圍
    location = geolocator.geocode(address, country_codes="TW")
    if location != None:
        lat = location.latitude
        lon = location.longitude
        return lat, lon
    else:
        msg = "Address not found."
        return msg


def gps_to_address(mark):
    location = geolocator.reverse(f"{mark[0]}, {mark[1]}", )
    ads = location.address
    return ads


def in_range(mark1, mark2, limit):
    distance = geodesic(mark1, mark2).km
    if distance > limit:
        return False
    else:
        return True
