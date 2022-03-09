import webbrowser
import folium
from geopy.geocoders import Nominatim

from pymongo import MongoClient
client = MongoClient('3.91.50.100',27017,
                     username='noE',
                     password='server_test')
db = client.exhibition_project

m = folium.Map([37.5710057, 126.9747532],tiles='cartodbpositron', zoom_start=15)
# 조건1 리스트의 딕셔너리 변수 중복
# 장소 중복 : 아라리오뮤지엄 탑동시네마
overlap_data = list(db.exhibition_info.find({'place':'아라리오뮤지엄 탑동시네마'},{'_id':False}))

# 조건 중복값이 있을 경우 -> 한 파일에 정보 몰아서 표기
# account['id']:account for account in accounts
# {}.values()


p_tags = []
for layer in overlap_data:
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
            
folium.Marker(location=[target_latitude, target_longitude], popup=popup_html, tooltip=target_place, icon=folium.Icon(color='blue')).add_to(m)


m.save(r'map1.html')
webbrowser.open_new_tab("map1.html")
print("완료")


