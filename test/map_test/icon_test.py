import folium
import webbrowser
from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent= 'Travel')
gallery_name = '서울시립미술관'
gallerys = geolocator.geocode(gallery_name)
gallery_latitude = gallerys.raw['lat']
gallery_longitude = gallerys.raw['lon']

#지도 배경 생성
# Zoom : zoom_start 최대 18, 최소 0
m = folium.Map([37.5666791, 126.9782914],tiles='cartodbpositron', zoom_start= 7)


# 이미지 아이콘 커스텀
custom_icon = folium.features.CustomIcon('C:/Users/82104/Desktop/220307/test/map_test/icon2.png', icon_size=(50,50),popup_anchor=(0, -15))
# CustomIcon(icon_anchor=(0, 85),shadow_image=shadow_image2,shadow_size=(150, 60),shadow_anchor=(30, 50))
# Create pop-up with html content
# popup = folium.Popup(pub_html, max_width=700)
popup_info = "<strong>html태그</strong>"

#마크 표시
folium.Marker(location = [gallery_latitude,gallery_longitude], popup = popup_info , icon = custom_icon).add_to(m)
#map1.html에 표시
m.save(r'map1.html')

# 파일 웹브라우저로 열기 #새로고침하는 방법은.. 셀레니움 써야하나..
webbrowser.open_new_tab("map1.html")
# 셀레니움 쓸때 열기, 새로고침
# driver = webdriver.Chrome(r'map1.html', options=option)
# driver.refresh()












