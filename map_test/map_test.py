# 패키지 설치 : geopy , folium
# map1.html에 지도 저장

import folium
from geopy.geocoders import Nominatim

gallery_name = '서울시립미술관'

geolocator = Nominatim(user_agent='Museum')
gallery = geolocator.geocode(gallery_name)
gal_latitude = gallery.raw['lat']
gal_longitude = gallery.raw['lon']

# 지도 배경 생성(이순신장군동상 기준)
# input으로 현재 위치 받아서 설정 예정
# zoom_start 최대 18, 최소 0
m = folium.Map([37.5710057, 126.9747532], zoom_start=15.5)

# 마크 표시
folium.Marker(location=[gal_latitude, gal_longitude], popup=gallery_name,
              icon=folium.Icon(color='red')).add_to(m)

# map1.html에 지도 표시
m.save(r'map1.html')
