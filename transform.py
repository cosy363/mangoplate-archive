from pyproj import Transformer
from geopy.geocoders import Nominatim

transformer = Transformer.from_crs('epsg:4326','epsg:3857')

def create_coord(address):
    geolocoder = Nominatim(user_agent = 'South Korea', timeout=None)
    geo = geolocoder.geocode(address)

    return str(geo.latitude), str(geo.longitude)

def get_url(search,address):
    # 지도 배율
    mag = str(4)

    # 주소 -> 좌표 변환
    lon, lat = create_coord(address)
    print(lon,lat)
    
    # x,y 좌표로 변환
    x, y = transformer.transform(float(lon), float(lat))

    return f"http://map.naver.com/p/search/{search}?c={x},{y},{mag},0,0,0,dh"


print(get_url("처가집부대고기","서울시 도봉구 도봉동 44-5"))

# print(transform(proj_WGS1984, proj_NAVER, 37.9051316, 127.0609492))


# 37.9051316 127.0609492