# 패키지 설치 : geopy , folium, pymongo
# map1.html에 지도 저장

import folium
from geopy.geocoders import Nominatim

from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.exhibition_info

#크롤링 place 리스트화
exhibition_infos= list(db.exhibition_info.find({},{'_id':False}))
all_place=[]
for exhibition_info in exhibition_infos:
    place_info = exhibition_info['place']
    all_place.append(place_info)
print(all_place)


# 지도 배경 생성(이순신장군동상 기준)
# input으로 현재 위치 받아서 설정 예정
# zoom_start 최대 18, 최소 0
m = folium.Map([37.5710057, 126.9747532],tiles='cartodbpositron', zoom_start=15)
# m = folium.Map([37.5710057, 126.9747532],tiles='stamenterrain', zoom_start=15.5)
# m = folium.Map([37.5710057, 126.9747532],tiles='stamentoner', zoom_start=15.5)



# 일반 전시 함수
# def mark_exhibition():
#
#     return
geolocator = Nominatim(user_agent='Exhibition')
for place in all_place:
 target = geolocator.geocode(place)
 print(target)
#  target_latitude = target.raw
#  target_longitude =
# print(gallery)
# gal_latitude = gallery.raw['lat']
# gal_longitude = gallery.raw['lon']
# # 파랑 i마크 표시
# folium.Marker(location=[gal_latitude, gal_longitude], popup=gallery_name, icon=folium.Icon(color='blue')).add_to(m)
#
# # 즐겨찾기 전시 함수
#
# gallery2 = geolocator.geocode(gallery_name2)
# gal_latitude2 = gallery2.raw['lat']
# gal_longitude2 = gallery2.raw['lon']
# # 빨강 별마크 표시
# folium.Marker(location=[gal_latitude2, gal_longitude2], popup=gallery_name, icon=folium.Icon(color='red', icon='star')).add_to(m)
# # map1.html에 지도 표시
# m.save(r'map1.html')



# # icon color
# folium.Marker(
#     [37.54461957910074, 127.05590699103249],
#     popup="<a href='https://zero-base.co.kr/' target=_'blink'>마커</a>",
#     tooltip='Zerobase',
#     icon=folium.Icon(
#         color='red',
#         icon_color='blue',
#         icon='cloud'
#     )
# ).add_to(m)




