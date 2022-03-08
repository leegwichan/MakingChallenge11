# 패키지 설치 : geopy , folium, pymongo
# map1.html에 지도 저장
# 테스트동안 import webbrowser(첫째줄)

import webbrowser
import folium
from geopy.geocoders import Nominatim

from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.exhibition_info

# # 지도 배경 생성(이순신장군동상 기준)
# # input으로 현재 위치 받아서 설정 예정
# # zoom_start 최대 18, 최소 0
m = folium.Map([37.5710057, 126.9747532],tiles='cartodbpositron', zoom_start=15)

#DB 추출
exhibition_infos= list(db.exhibition_info.find({},{'_id':False}))
# 타이틀, 장소, 위도, 경도, 이미지
for exhibition_info in exhibition_infos:
    if "latitude" in exhibition_info:
        target_title = exhibition_info['title']
        target_place = exhibition_info['place']
        target_image = exhibition_info['image_link']
        target_latitude = exhibition_info['latitude']
        target_longitude = exhibition_info['longitude']
        """
        팝업창 구현부

        조건 1: 이미 이미지가 있으면 추가 덧붙임
        popup_section = "<div width='500px' href='#' target=_'blink' scr='{image}'>{title},{place}</div>".format(image=target_image,title =target_title, place=target_place)
        # "a의 값: {zero}, c의 값: {one}" .format(zero = a, one = c)
    
        """
        folium.Marker(location=[target_latitude, target_longitude], popup=popup_section, icon=folium.Icon(color='blue')).add_to(m)
m.save(r'map1.html')
webbrowser.open_new_tab("map1.html")
print("완료")

"""
##마커 관련 참고

# 즐겨찾기 전시 빨강 별마크 표시
folium.Marker(location=[gal_latitude2, gal_longitude2], popup=gallery_name2, icon=folium.Icon(color='red', icon='star')).add_to(g1)

# 이미지 아이콘 커스텀
custom_icon = folium.features.CustomIcon('C:/Users/82104/Desktop/220307/test/map_test/icon2.png', icon_size=(50,50),popup_anchor=(0, -15))
# CustomIcon(icon_anchor=(0, 85),shadow_image=shadow_image2,shadow_size=(150, 60),shadow_anchor=(30, 50))
# Create pop-up with html content
# popup = folium.Popup(pub_html, max_width=700)

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