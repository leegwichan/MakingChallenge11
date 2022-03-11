# 패키지 설치 : geopy , folium, pymongo, flask
# map1.html에 지도 저장
# 테스트동안 import webbrowser(첫째줄)

from flask import Flask, render_template, jsonify, request
app = Flask(__name__)

import webbrowser
import folium
from geopy.geocoders import Nominatim
from collections import Counter

from pymongo import MongoClient
client = MongoClient('3.91.50.100',27017,
                     username='noE',
                     password='server_test')
db = client.exhibition_project

@app.route('/')
def home():
   return render_template('geolocation.html')

@app.route('/map', methods=['POST'])
def test_post():
   latitude_receive = request.form['latitude_give']
   longitude_receive = request.form['longitude_give']
   
   m = folium.Map([latitude_receive, longitude_receive],tiles='cartodbpositron', zoom_start=15)
   m.save(r'exhibition_map.html')
   # return render_template('exhibition_map.html')
   # return jsonify({'msg': '현재 위치로 설정'})
   # return jsonify({'result':"success", 'msg': "맵저장완료"})


if __name__ == '__main__':  
   app.run('0.0.0.0',port=5000,debug=True)