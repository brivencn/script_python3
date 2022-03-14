from math import radians, cos, sin, asin, sqrt
from geopy.distance import geodesic


# 公式计算两点间距离（km）

def getdistance(lng1, lat1, lng2, lat2):
    # lng1,lat1,lng2,lat2 = (120.12802999999997,30.28708,115.86572000000001,28.7427)
    lng1, lat1, lng2, lat2 = map(radians, [float(lng1), float(lat1), float(lng2), float(lat2)])  # 经纬度转换成弧度
    dlon = lng2 - lng1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    distance = 2 * asin(sqrt(a)) * 6371 * 1000  # 地球平均半径，6371km
    distance = round(distance / 1000, 6)
    return distance

def geodistance(lng1, lat1, lng2, lat2):
    distance = geodesic("{},{}".format(lat1, lng1), "{},{}".format(lat2, lng2))
    return distance

if __name__ == '__main__':
    print(getdistance('106.494112', '29.832802', '106.555254', '29.558581'))
    print(geodistance('106.494112', '29.832802', '106.555254', '29.558581').km)