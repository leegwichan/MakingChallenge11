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


# 타이틀, 장소, 위도, 경도
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
            
        
        # 중복 빨간마크
        else :
            p_tags =[]
            target_latitude = data['latitude']
            target_longitude = data['longitude']
            target_title = data['title']
            target_place = data['place']
            target_period = data['start_date'] +" ~ "+ data['end_date']
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



        # 팝업창 구현부
        # 조건 1: 이미 이미지가 있으면 추가 덧붙임
        # # Define html inside marker pop-up
        # pub_html = folium.Html(f"""<p style="text-align: center;"><span style="font-family: Didot, serif; font-size: 21px;">{name}</span></p>
        # <p style="text-align: center;"><iframe src={insta_post}embed width="240" height="290" frameborder="0" scrolling="auto" allowtransparency="true"></iframe>
        # <p style="text-align: center;"><a href={website} target="_blank" title="{name} Website"><span style="font-family: Didot, serif; font-size: 17px;">{name} Website</span></a></p>
        # <p style="text-align: center;"><a href={directions} target="_blank" title="Directions to {name}"><span style="font-family: Didot, serif; font-size: 17px;">Directions to {name}</span></a></p>
        # """, script=True)    

"""
##마커 관련 참고

# 즐겨찾기 전시 빨강 별마크 표시
folium.Marker(location=[gal_latitude2, gal_longitude2], popup=gallery_name2, icon=folium.Icon(color='red', icon='star')).add_to(g1)

# 이미지 아이콘 커스텀, 위치
custom_icon = folium.features.CustomIcon('C:/Users/82104/Desktop/220307/test/map_test/icon2.png', icon_size=(50,50),popup_anchor=(0, -15))
# CustomIcon(icon_anchor=(0, 85),shadow_image=shadow_image2,shadow_size=(150, 60),shadow_anchor=(30, 50))

#마크 표시
folium.Marker(location = [gallery_latitude,gallery_longitude], popup = "html 내용" , icon = custom_icon).add_to(m)
"""

"""
# icon 사용예시
folium.Marker(
    [37.54461957910074, 127.05590699103249],
    popup="<a href='https://zero-base.co.kr/' target=_'blink'>마커</a>",
    tooltip='Zerobase',
    icon=folium.Icon(
        color='red',
        icon_color='blue',
        icon='cloud'
    )
).add_to(m)
"""

"""
##선택창
#마커코드 작성시 .add_to(m)대신 그룹 기재
from folium import plugins
gs = folium.FeatureGroup(name='Groups')
m.add_child(gs)
g1 = plugins.FeatureGroupSubGroup(gs, 'Group1')
m.add_child(g1)
folium.LayerControl(collapsed=False).add_to(m)
m.save(r'map1.html')
"""

"""
# 파일 웹브라우저로 열기
webbrowser.open_new_tab("map1.html")
# 셀레니움 쓸때 열기, 새로고침
# driver = webdriver.Chrome(r'map1.html', options=option)
# driver.refresh()
"""