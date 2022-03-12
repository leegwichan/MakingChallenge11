# 패키지 설치 : geopy , folium, pymongo
# map1.html에 지도 저장
# 테스트동안 import webbrowser(첫째줄)

from collections import Counter
import webbrowser
import folium
from geopy.geocoders import Nominatim

from pymongo import MongoClient
client = MongoClient('3.91.50.100',27017,
                     username='noE',
                     password='server_test')
db = client.exhibition_project

total_data = list(db.exhibition_info.find({},{'_id':False}))

# 7일차에 정리함

overlay_check = []
for data in total_data:
    overlay_check.append(data['place'])

overlap_place = []
result = Counter(overlay_check)
for key, value in result.items():
    if value >= 2:
        overlap_place.append(key)
print(overlap_place)

for data in total_data:
    if "latitude" in data:
        if(data['place'] in overlap_place):
            print(data['place'])

