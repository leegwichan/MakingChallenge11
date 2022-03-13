from bson.json_util import dumps
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

#지도 관련
import folium
from geopy.geocoders import Nominatim
from collections import Counter

from pymongo import MongoClient
client = MongoClient('18.208.182.249',27017,
                     username='noE',
                     password='server_test')
db = client.exhibition_project



# html 받아오는 부분
@app.route('/')
def home():
    return render_template('main.html')



## 지도 관련부분 버튼

#현재 위치 검색
@app.route('/myposition', methods=['POST'])
def my_position():
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


# 지도 검색 부분
@app.route('/setposition', methods=['POST'])
def set_position():
   address1_recieve = request.form['address1_give'] #"광주시"
   address2_recieve = request.form['address2_give'] #"북구"
   # user = db.users.find_one({'name':'bobby'})
   # same_ages = list(db.users.find({'age':21},{'_id':False}))
   #새로운 db에 동시에 만족하는것 추출
   # latitude_receive = request.form['latitude_give']
   # longitude_receive = request.form['longitude_give']


   # title_receive = request.form['title_give']
   # print(title_receive)
   return jsonify({'result':'success', 'msg': '이 요청은 지도검색 POST!'})



##메인페이지 로그인한 상태에서 동작
@app.route('/mycategory', methods=['POST'])
def test_post():
   key_recieve = request.form['key_give']
   user_data = db.login_info.find_one({'key':key_recieve})
   user_category = user_data["CATEGORY"]
   return jsonify({'result':'success', 'msg': '이 요청은 POST!', "selected_catgy":user_category})



# 새로고침 전시 기본 리스트업(html ajax 수정완료)
@app.route('/list', methods=['GET'])
def get_list():
   exhibition_list = list(db.exhibition_info.aggregate([{"$sample":{ "size": 20}}]))
   return jsonify({'show_list': dumps(exhibition_list)})


## 카테고리 관련부분 버튼

# 관심카테고리 속 다했어요 버튼 부분
@app.route('/multi_s_list', methods=['POST'])
def get_selectlist():
   class_receive = request.form['class_give']
   class_receive = request.form['key_give']
   selected_list = list(db.exhibition_info.aggregate([{"$match": {"class":class_receive}},{"$sample":{"size": 20}}]))
   #클라이언트에 클래스요소 검색후 반환
   #클래서 변경부분 수정->DB저장
   # db.users.update_one({'name':'bobby'},{'$set':{'age':19}})
   # return jsonify({'show_list':dumps(selected_list), 'msg': '이 요청은 관심카테고리선택 POST!'})


   key_recieve = request.form['key_give']
   user_data = db.login_info.find_one({'key':key_recieve})


# 전시 카데고리 선택 리스트업 시작
# main.html의 onclick, value 부분 수정해주세요~ 
@app.route('/select_list', methods=['GET'])
def get_exhibitionlist():
   class_receive = request.args.get('class_give')
   selected_list = list(db.exhibition_info.aggregate([{"$match": {"class":class_receive}},{"$sample":{"size": 20}}]))
   return jsonify({'show_list':dumps(selected_list), 'msg': '이 요청은 전시 GET!'})

# @app.route('/museum_list', methods=['GET'])
# def get_museumlist():
#    class_receive = request.args.get('class_give')
#    print(class_receive)
#    # exhibition_list = list(db.exhibition_info.aggregate([{"$sample":{ "size": 20}}]))
#    return jsonify({'result':'success', 'msg': '이 요청은 뮤지엄 GET!'})

# @app.route('/childs_list', methods=['GET'])
# def get_childrenlist():
#    class_receive = request.args.get('class_give')
#    print(class_receive)
#    # exhibition_list = list(db.exhibition_info.aggregate([{"$sample":{ "size": 20}}]))
#    return jsonify({'result':'success', 'msg': '이 요청은 아동체험전 GET!'})

# @app.route('/evenfestival_list', methods=['GET'])
# def get_eflist():
#    class_receive = request.args.get('class_give')
#    print(class_receive)
#    # exhibition_list = list(db.exhibition_info.aggregate([{"$sample":{ "size": 20}}]))
#    return jsonify({'result':'success', 'msg': '이 요청은 evenfestiva GET!'})

# @app.route('/class_list', methods=['GET'])
# def get_classlist():
#    class_receive = request.args.get('class_give')
#    print(class_receive)
#    # exhibition_list = list(db.exhibition_info.aggregate([{"$sample":{ "size": 20}}]))
#    return jsonify({'result':'success', 'msg': '이 요청은 클래스리스트 GET!'})

# 전시 카데고리 선택 리스트업 끝








if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
