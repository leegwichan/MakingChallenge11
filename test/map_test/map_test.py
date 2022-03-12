# 패키지 설치 : geopy , folium, pymongo
# map1.html에 지도 저장
# 테스트동안 import webbrowser(첫째줄)

import webbrowser
import folium
from geopy.geocoders import Nominatim
from collections import Counter

from pymongo import MongoClient
client = MongoClient('18.208.182.249',27017,
                     username='noE',
                     password='server_test')
db = client.exhibition_project


# 지도 생성 : input으로 위치 받아서 설정 예정(기본값 이순신장군동상 기준), zoom_start 최대 18, 최소 0
m = folium.Map([37.5710057, 126.9747532],tiles='cartodbpositron', zoom_start=15)


total_data = list(db.exhibition_info.find({},{'_id':False}))

# 여러 전시 운영하는 장소 변수 : overlap_place
overlap_check = []
for data in total_data:
    overlap_check.append(data['place'])

overlap_place = []
result = Counter(overlap_check)
for key, value in result.items():
    if value >= 2:
        overlap_place.append(key)

# 한 장소에 여러 종류 전시(구름아이콘)   
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
    
    folium.Marker(location=[target_latitude, target_longitude], popup=popup_html, tooltip=target_place, icon=folium.Icon(color='blue', icon_color='lightgray',icon='cloud')).add_to(m)


# 한 장소에 1종류 전시
for data in total_data:
    if "latitude" in data:
        if(data['place'] not in overlap_place):
            target_title = data['title']
            target_place = data['place']
            target_period = data['start_date'] +" ~ "+ data['end_date']
            target_latitude = data['latitude']
            target_longitude = data['longitude']
            
            summary_info = folium.Html(f"""<div style = "text-align: center; ">
                                                <p style="font-weight:bold;">{target_title}<br>{target_period}</p>
                                                in {target_place}
                                        </div>""", script = True)
            popup_html = folium.Popup(summary_info,max_width=500)
            
            folium.Marker(location=[target_latitude, target_longitude], popup=popup_html, tooltip=target_place, icon=folium.Icon(color='blue')).add_to(m)
            

m.save(r'map1.html')
webbrowser.open_new_tab("map1.html")
print("완료")


 
"""
# 커스텀 마커 정의
custom_icon = folium.features.CustomIcon('C:/Users/82104/Desktop/220307/test/map_test/icon2.png', icon_size=(50,50),popup_anchor=(0, -15))

# 커스텀 마커 사용
folium.Marker(location = [gallery_latitude,gallery_longitude], popup = "html 내용" , icon = custom_icon).add_to(m)

# 선택창 : 마커코드 작성시 .add_to(m)에 m대신 그룹 넣기
from folium import plugins
gs = folium.FeatureGroup(name='Groups')
m.add_child(gs)
g1 = plugins.FeatureGroupSubGroup(gs, 'Group1')
m.add_child(g1)
folium.LayerControl(collapsed=False).add_to(m)
m.save(r'map1.html')

"""