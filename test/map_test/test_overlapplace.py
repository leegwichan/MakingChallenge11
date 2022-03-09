# 패키지 설치 : geopy , folium, pymongo
# map1.html에 지도 저장
# 테스트동안 import webbrowser(첫째줄)

import webbrowser
import folium
from geopy.geocoders import Nominatim
from collections import Counter

from pymongo import MongoClient
client = MongoClient('3.91.50.100',27017,
                     username='noE',
                     password='server_test')
db = client.exhibition_project


# # 지도 배경 생성(이순신장군동상 기준)
# # input으로 현재 위치 받아서 설정 예정
# # zoom_start 최대 18, 최소 0
m = folium.Map([37.5710057, 126.9747532],tiles='cartodbpositron', zoom_start=15)


total_data = list(db.exhibition_info.find({},{'_id':False}))

# 여러 전시 운영하는 장소 변수 : overlap_place
overlay_check = []
for data in total_data:
    overlay_check.append(data['place'])

overlap_place = []
result = Counter(overlay_check)
for key, value in result.items():
    if value >= 2:
        overlap_place.append(key)

#중복조건으로 DB출력
for place in overlap_place:
    overlap_data = list(db.exhibition_info.find({'place':place},{'_id':False}))
    p_tags = []
    for layer in overlap_data:
        
        if "latitude" in layer:
            target_latitude = layer['latitude']
            target_longitude = layer['longitude']
            target_title = layer['title']
            target_place = layer['place']
            target_period = layer['start_date'] +" ~ "+ layer['end_date']
            target_info = f"""<p style="font-weight:bold;">{target_title}<br>{target_period}</p>"""
            p_tags.append(target_info)
    p_tags=''.join(p_tags)    
    full_text = f"""<div style = "text-align: center; ">{p_tags}
                        in {target_place}
                    </div>"""

    summary_info = folium.Html(f"""{full_text}""", script = True)
    popup_html = folium.Popup(summary_info,max_width=500)

    folium.Marker(location=[target_latitude, target_longitude], popup=popup_html, tooltip=target_place, icon=folium.Icon(color='red')).add_to(m)
        

m.save(r'map1.html')
webbrowser.open_new_tab("map1.html")
print("완료")





