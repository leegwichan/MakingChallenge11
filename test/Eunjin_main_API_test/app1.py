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
   return render_template('templates/geolocation.html')
   #  return render_template('main.html')



## 지도 관련부분 버튼 시작 ##

##### 지도함수 #####
# 지도 좌표설정
def make_map(latitude, longitude):
    m = folium.Map([latitude, longitude],
                   tiles='cartodbpositron', zoom_start=15)
    return m


# 북마크 장소값 모음 함수
def make_bmplace(key):
    user_data = db.login_info.find_one({'KEY': key})
    bmark_id = user_data['BOOKMARK']  # list형태
    bmark_place = []
    for target_id in bmark_id:
        place = db.exhibition_info.find_one({'id': target_id})["place"]
        bmark_place.append(place)
    return bmark_place



# 현재 위치 검색(북마크 수정 필요!)
@app.route('/myposition', methods=['POST'])
def my_position():
    latitude_receive = request.form['latitude_give']
    longitude_receive = request.form['longitude_give']

    total_data = list(db.exhibition_info.find({}, {'_id': False}))

    # 여러 전시 운영하는 장소의 좌표 리스트 : overlap_coordinate
    overlap_check = []
    for data in total_data:
        if "latitude" in data and "longitude" in data:
            overlap_data = (data['latitude'], data['longitude'])
            overlap_check.append(overlap_data)

    overlap_coordinate = []
    result = Counter(overlap_check)
    for key, value in result.items():
        if value >= 2:
            overlap_coordinate.append(key)

    # 한 장소에 1종류 전시
    for data in total_data:
        if "latitude" in data:
            if((data['latitude'], data['longitude']) not in overlap_coordinate):
                target_title = data['title']
                target_place = data['place']
                target_period = data['start_date'] + " ~ " + data['end_date']
                target_latitude = data['latitude']
                target_longitude = data['longitude']

                summary_info = folium.Html(f"""<div style = "text-align: center; ">
                                                   <p style="color:gray;">
                                                   <span style="font-weight:bold; color:#080808">{target_title}
                                                   <br>{target_period}</span>
                                                   <br>in {target_place}
                                                   </p>
                                          </div>""", script=True)
                popup_html = folium.Popup(summary_info, max_width=500)
                folium.Marker(location=[target_latitude, target_longitude], popup=popup_html,
                              tooltip=target_place, icon=folium.Icon(color='blue')).add_to(map)

    # 한 장소에 여러 종류 전시(구름아이콘)
    for coordinate in overlap_coordinate:
        overlap_coordinate = list(db.exhibition_info.find(
            {'latitude': coordinate[0], 'longitude': coordinate[1]}, {'_id': False}))
        popup_msg = []
        for overlap_one in overlap_coordinate:
            target_latitude = overlap_one['latitude']
            target_longitude = overlap_one['longitude']
            target_title = overlap_one['title']
            target_place = overlap_one['place']
            target_period = overlap_one['start_date'] + \
                " ~ " + overlap_one['end_date']

            target_info = f"""<p style="color:gray;">
                                 <span style="font-weight:bold; color:#080808">{target_title}<br>{target_period}</span>
                                <br>in {target_place}
                            </p>"""
            popup_msg.append(target_info)

        popup_msg = ''.join(popup_msg)
        full_text = f"""<div style = "text-align: center; ">{popup_msg}
                        </div>"""

        summary_info = folium.Html(f"""{full_text}""", script=True)
        popup_html = folium.Popup(summary_info, max_width=500)
        folium.Marker(location=[target_latitude, target_longitude], popup=popup_html,
                      tooltip=target_place, icon=folium.Icon(color='blue', icon='cloud')).add_to(map)

    map.save(
        r'C:/Users/82104/Desktop/220308/test/map_test/map_api_test/templates/position_map.html')
    webbrowser.open_new_tab(
        'C:/Users/82104/Desktop/220308/test/map_test/map_api_test/templates/position_map.html')
    # map.save(r'sftp://ubuntu@18.208.182.249/home/ubuntu/MakingChallenge11/exhibi-dev/templates/position_map.html')
    return jsonify({'result': 'success'})


# 지도 검색 부분(북마크 수정 필요!)
@app.route('/setposition', methods=['POST'])
def set_position():
    # 베이스맵 생성
    address1_recieve = request.form['address1_give']  # "광주시"
    address2_recieve = request.form['address2_give']  # "북구"
    set_location = db.region_info.find_one(
        {'address_class1': address1_recieve, 'address_class2': address2_recieve})
    map = make_map(set_location['latitude'], set_location['longitude'])

    # 마이로케이션이랑 동일한 로직
    total_data = list(db.exhibition_info.find({}, {'_id': False}))

    # 여러 전시 운영하는 장소의 좌표 리스트 : overlap_coordinate
    overlap_check = []
    for data in total_data:
        if "latitude" in data and "longitude" in data:
            overlap_data = (data['latitude'], data['longitude'])
            overlap_check.append(overlap_data)

    overlap_coordinate = []
    result = Counter(overlap_check)
    for key, value in result.items():
        if value >= 2:
            overlap_coordinate.append(key)

    # 한 장소에 1종류 전시
    for data in total_data:
        if "latitude" in data:
            if((data['latitude'], data['longitude']) not in overlap_coordinate):
                target_title = data['title']
                target_place = data['place']
                target_period = data['start_date'] + " ~ " + data['end_date']
                target_latitude = data['latitude']
                target_longitude = data['longitude']

                summary_info = folium.Html(f"""<div style = "text-align: center; ">
                                                   <p style="color:gray;">
                                                   <span style="font-weight:bold; color:#080808">{target_title}
                                                   <br>{target_period}</span>
                                                   <br>in {target_place}
                                                   </p>
                                          </div>""", script=True)
                popup_html = folium.Popup(summary_info, max_width=500)
                folium.Marker(location=[target_latitude, target_longitude], popup=popup_html,
                              tooltip=target_place, icon=folium.Icon(color='blue')).add_to(map)

    # 한 장소에 여러 종류 전시(구름아이콘)
    for coordinate in overlap_coordinate:
        overlap_coordinate = list(db.exhibition_info.find(
            {'latitude': coordinate[0], 'longitude': coordinate[1]}, {'_id': False}))
        popup_msg = []
        for overlap_one in overlap_coordinate:
            target_latitude = overlap_one['latitude']
            target_longitude = overlap_one['longitude']
            target_title = overlap_one['title']
            target_place = overlap_one['place']
            target_period = overlap_one['start_date'] + \
                " ~ " + overlap_one['end_date']

            target_info = f"""<p style="color:gray;">
                                 <span style="font-weight:bold; color:#080808">{target_title}<br>{target_period}</span>
                                <br>in {target_place}
                            </p>"""
            popup_msg.append(target_info)

        popup_msg = ''.join(popup_msg)
        full_text = f"""<div style = "text-align: center; ">{popup_msg}
                        </div>"""

        summary_info = folium.Html(f"""{full_text}""", script=True)
        popup_html = folium.Popup(summary_info, max_width=500)
        folium.Marker(location=[target_latitude, target_longitude], popup=popup_html,
                      tooltip=target_place, icon=folium.Icon(color='blue', icon='cloud')).add_to(map)

    map.save(
        r'C:/Users/82104/Desktop/220308/test/map_test/map_api_test/templates/new_map.html')
    webbrowser.open_new_tab(
        'C:/Users/82104/Desktop/220308/test/map_test/map_api_test/templates/new_map.html')
    # map.save(r'sftp://ubuntu@18.208.182.249/home/ubuntu/MakingChallenge11/exhibi-dev/templates/new_map.html')
    return jsonify({'result': 'success'})


#메인페이지 로그인한 상태에서 동작
@app.route('/mycategory', methods=['POST'])
def test_post():
   user_key = request.form['key_give']
   user_data = db.login_info.find_one({'key':user_key})
   user_category = user_data["CATEGORY"]
   return jsonify({'msg': '이 요청은 POST!', "selected_catgy":user_category})


# 새로고침 전시 기본 리스트업(html ajax 수정완료)
@app.route('/list', methods=['GET'])
def get_list():
   exhibition_list = list(db.exhibition_info.aggregate([{"$sample":{ "size": 20}}]))
   return jsonify({'show_list': dumps(exhibition_list)})


## 카테고리 관련부분 버튼 시작 ##

# 관심카테고리 속 다했어요 버튼 부분
@app.route('/multi_s_list', methods=['POST'])
def get_selectlist():
   class_receive = request.form['class_give']
   key_receive = request.form['key_give']

   # 새로운 리스트정보
   selected_list = list(db.exhibition_info.aggregate([{"$match": {"class":class_receive}},{"$sample":{"size": 20}}]))

   # DB저장
   db.login_info.update_one({'key':key_receive},{'$set':{'CATEGORY':class_receive}})
   user_name = db.login_info.find_one({"KEY":key_receive})["NAME"]
   msg = user_name + "님의 관심카테고리가 변경되었습니다."

   return jsonify({'show_list':dumps(selected_list), 'msg': msg })



# 전시 카데고리 선택 리스트업 시작
# main.html의 onclick, value 부분 수정해주세요~ 
@app.route('/select_list', methods=['GET'])
def get_exhibitionlist():
   class_receive = request.args.get('class_give')
   selected_list = list(db.exhibition_info.aggregate([{"$match": {"class":class_receive}},{"$sample":{"size": 20}}]))
   return jsonify({'show_list':dumps(selected_list), 'msg': '이 요청은 전시 GET!'})

## 카테고리 관련부분 버튼 끝 ##


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
