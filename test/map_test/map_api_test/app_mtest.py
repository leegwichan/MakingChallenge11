# 패키지 설치 : geopy , folium, pymongo, flask
# map1.html에 지도 저장
# 테스트동안 import webbrowser(첫째줄)

from flask import Flask, render_template, jsonify, request
app = Flask(__name__)

# import webbrowser
import folium
from geopy.geocoders import Nominatim
from collections import Counter

from pymongo import MongoClient
client = MongoClient('18.208.182.249',27017,
                     username='noE',
                     password='server_test')
db = client.exhibition_project

@app.route('/')
def home():
   return render_template('geolocation.html')

@app.route('/exhibi_map', methods=['POST'])
def test_post():
   latitude_receive = request.form['latitude_give']
   longitude_receive = request.form['longitude_give']
   
   m = folium.Map([latitude_receive, longitude_receive],tiles='cartodbpositron', zoom_start=15)

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
               
   m.save(r'C:/Users/82104/Desktop/220308/test/map_test/map_api_test/templates/exhibition_map.html')
   # webbrowser.open_new_tab('C:/Users/82104/Desktop/220308/test/map_test/map_api_test/templates/exhibition_map.html')
   # m.save(r'sftp://ubuntu@18.208.182.249/home/ubuntu/MakingChallenge11/exhibi-dev/templates/exhibition_map.html')
   return jsonify({'result':'success'})


if __name__ == '__main__':  
   app.run('0.0.0.0',port=5000,debug=True)