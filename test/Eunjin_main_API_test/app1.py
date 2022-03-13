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



# 각 html에 맞는 route가 있으니 필요에 따라 주석 제거하면서 실행해 보시면 됩니다!

# html 받아오는 부분
@app.route('/')
def home():
    return render_template('main.html')





## 지도 관련부분 버튼

#현재 위치 검색
@app.route('/myposition', methods=['POST'])
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


# 지도 검색 부분
@app.route('/setposition', methods=['POST'])
def test_post():
   title_receive = request.form['title_give']
   print(title_receive)
   return jsonify({'result':'success', 'msg': '이 요청은 지도검색 POST!'})





## 카테고리 관련부분 버튼

# 관심카테고리 속 다했어요 버튼 부분
@app.route('/test', methods=['POST'])
def test_post():
   title_receive = request.form['title_give']
   print(title_receive)
   return jsonify({'result':'success', 'msg': '이 요청은 지도검색 POST!'})


# 새로고침 전시 기본 리스트업(html ajax 수정완료)
@app.route('/list', methods=['GET'])
def get_list():
   exhibition_list = list(db.exhibition_info.aggregate([{"$sample":{ "size": 20}}]))
   return jsonify({'show_list': dumps(exhibition_list)})


# 전시 카데고리 선택 리스트업 시작
# main.html의 inclick, value 부분 수정해주세요~ 
@app.route('/exhibition_list', methods=['GET'])
def test_get():
   class_receive = request.args.get('class_give')
   print(class_receive)
   # exhibition_list = list(db.exhibition_info.aggregate([{"$sample":{ "size": 20}}]))
   return jsonify({'result':'success', 'msg': '이 요청은 전시 GET!'})

@app.route('/museum_list', methods=['GET'])
def test_get():
   class_receive = request.args.get('class_give')
   print(class_receive)
   # exhibition_list = list(db.exhibition_info.aggregate([{"$sample":{ "size": 20}}]))
   return jsonify({'result':'success', 'msg': '이 요청은 뮤지엄 GET!'})

@app.route('/childs_list', methods=['GET'])
def test_get():
   class_receive = request.args.get('class_give')
   print(class_receive)
   # exhibition_list = list(db.exhibition_info.aggregate([{"$sample":{ "size": 20}}]))
   return jsonify({'result':'success', 'msg': '이 요청은 아동체험전 GET!'})

@app.route('/evenfestival_list', methods=['GET'])
def test_get():
   class_receive = request.args.get('class_give')
   print(class_receive)
   # exhibition_list = list(db.exhibition_info.aggregate([{"$sample":{ "size": 20}}]))
   return jsonify({'result':'success', 'msg': '이 요청은 evenfestiva GET!'})

@app.route('/class_list', methods=['GET'])
def test_get():
   class_receive = request.args.get('class_give')
   print(class_receive)
   # exhibition_list = list(db.exhibition_info.aggregate([{"$sample":{ "size": 20}}]))
   return jsonify({'result':'success', 'msg': '이 요청은 클래스리스트 GET!'})

# 전시 카데고리 선택 리스트업 끝








# # api

# # 회원가입
# @app.route('/sign_up', methods=['POST'])
# def sign_up_post():

#     session_key = ''

#     ID_receive = request.form['ID_give']
#     PASSWORD_receive = request.form['PASSWORD_give']
#     NAME_receive = request.form['NAME_give']
#     PHONE_NUMBER_receive = request.form['PHONE_NUMBER_give']
#     CATEGORY_receive = request.form['INTEREST_CATEGORY_give']

#     # 아이디의 아스키 코드를 key 값으로 설정
#     len_id = len(ID_receive)
#     for i in range(len_id):
#         session_key += str(ord(str((ID_receive[i]))))

#     doc = {

#         'ID': ID_receive,
#         'PASSWORD': PASSWORD_receive,
#         'NAME': NAME_receive,
#         'PHONE_NUMBER': PHONE_NUMBER_receive,
#         'CATEGORY': CATEGORY_receive,
#         'KEY' : session_key

#     }
#     db.login_info.insert_one(doc)
#     return jsonify({'msg': 'COMPLETE'})




# # 중복 확인란
# @app.route('/id_overlap', methods=['POST'])
# def overlap_get():
#     find_ID_receive = request.form['ID_give']
#     find_phone_receive = request.form['PHONE_NUMBER_give']

#     same_ID = list(db.login_info.find({'ID': find_ID_receive},{'_id':False}))
#     same_PHONE = list(db.login_info.find({'PHONE_NUMBER': find_phone_receive},{'_id':False}))

#     # 중복 확인 조건문


#     return jsonify({'ID_result':same_ID, 'Phone_result':same_PHONE})




# # 로그인 부분
# # 로그인 부분
# # 로그인 부분
# # 로그인 부분

# @app.route('/login_page')
# def login_page():
#     return render_template('login.html')


# # db에 저장된 목록 받아오기 --> 로그인을 위해서
# @app.route('/login', methods=['GET'])
# def sign_up_get():
#     member_list = list(db.login_info.find({}, {'_id': False}))
#     return jsonify({'all_member_list': member_list})



# # 회원 정보 수정

# @app.route('/user_edit')
# def edit_page():
#     return render_template('my_info_edit.html')


# # 회원 정보 조회
# @app.route('/user_view', methods=['POST'])
# def user_view():
#     key_receive = request.form['key_give']
#     user_list = list(db.login_info.find({}, {'_id': False}))
#     user = user_list[int(key_receive)]
#     return jsonify({'user': user})

# # 회원 정보 수정 api
# @app.route('/user_edit', methods=['POST'])
# def user_info_edit():

#     # 정보 받아오기
#     my_info_receive = request.form.get('my_info_give',False)
#     key_receive = request.form['key_give']

#     # 바꿀 아이디 찾기
#     user_list = list(db.login_info.find({}, {'_id': False}))
#     user = user_list[int(key_receive)]
#     user_id = user['ID']

#     # 찾은 아이디에 딕셔너리를 바꾸자
#     db.login_info.delete_one({'ID':user_id})
#     user = my_info_receive
#     db.login_info.insert_one(user)
#     # db.login_info.update_one({'ID':user_id},{'$set':my_info_receive})

#     user = user_list[int(key_receive)]
#     return jsonify({'msg': '완료되었습니다'})




if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
