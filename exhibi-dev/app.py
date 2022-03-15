# flask import
from collections import Counter
from geopy.geocoders import Nominatim
import folium
from bson.json_util import dumps
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
import random
import string
from pymongo import MongoClient
from flask import Flask, render_template, jsonify, request
app = Flask(__name__)
# pymongo import
client = MongoClient('18.208.182.249', 27017,
                     username='noE',
                     password='server_test')
db = client.exhibition_project
# random 관련 import

# password 찾기 관련 import

# JSON 직렬화 오류

# 지도 관련 import

# 리스트업 관련 import


# html 받아오는 부분
@app.route('/')
def home():
    return render_template('main.html')

# html 받아오는 부분 # 기본맵


@app.route('/exhibi_map')
def map():
    return render_template('exhibition_map.html')

# html 받아오는 부분 # 회원가입 부분


@app.route('/join')
def join_Loadpage():
    return render_template('join.html')

# html 받아오는 부분 # 로그인 부분


@app.route('/login_page')
def login_page():
    return render_template('login.html')


#######메인 관련#########

## 지도 관련부분 버튼 시작 ##

# 현재 위치 검색(수정필요!)
@app.route('/myposition', methods=['POST'])
def my_position():
    latitude_receive = request.form['latitude_give']
    longitude_receive = request.form['longitude_give']

    m = folium.Map([latitude_receive, longitude_receive],
                   tiles='cartodbpositron', zoom_start=15)

    total_data = list(db.exhibition_info.find({}, {'_id': False}))

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
        overlap_data = list(db.exhibition_info.find(
            {'place': place}, {'_id': False}))
        p_tags = []
        for layer in overlap_data:
            if "latitude" in layer:
                target_latitude = layer['latitude']
                target_longitude = layer['longitude']
                target_title = layer['title']
                target_place = layer['place']
                target_period = layer['start_date'] + " ~ " + layer['end_date']

                target_info = f"""<p style="font-weight:bold;">{target_title}<br>{target_period}</p>"""
                p_tags.append(target_info)

        p_tags = ''.join(p_tags)
        full_text = f"""<div style = "text-align: center; ">{p_tags}
                           in {target_place}
                     </div>"""

        summary_info = folium.Html(f"""{full_text}""", script=True)
        popup_html = folium.Popup(summary_info, max_width=500)

        folium.Marker(location=[target_latitude, target_longitude], popup=popup_html, tooltip=target_place, icon=folium.Icon(
            color='blue', icon_color='lightgray', icon='cloud')).add_to(m)

    # 한 장소에 1종류 전시
    for data in total_data:
        if "latitude" in data:
            if(data['place'] not in overlap_place):
                target_title = data['title']
                target_place = data['place']
                target_period = data['start_date'] + " ~ " + data['end_date']
                target_latitude = data['latitude']
                target_longitude = data['longitude']

                summary_info = folium.Html(f"""<div style = "text-align: center; ">
                                                   <p style="font-weight:bold;">{target_title}<br>{target_period}</p>
                                                   in {target_place}
                                          </div>""", script=True)
                popup_html = folium.Popup(summary_info, max_width=500)

                folium.Marker(location=[target_latitude, target_longitude], popup=popup_html,
                              tooltip=target_place, icon=folium.Icon(color='blue')).add_to(m)

    m.save(r'C:/Users/82104/Desktop/220308/test/map_test/map_api_test/templates/exhibition_map.html')
    # webbrowser.open_new_tab('C:/Users/82104/Desktop/220308/test/map_test/map_api_test/templates/exhibition_map.html')
    # m.save(r'sftp://ubuntu@18.208.182.249/home/ubuntu/MakingChallenge11/exhibi-dev/templates/exhibition_map.html')
    return jsonify({'result': 'success'})


# 지도 검색 부분(수정필요!)
@app.route('/setposition', methods=['POST'])
def set_position():
    address1_recieve = request.form['address1_give']  # "광주시"
    address2_recieve = request.form['address2_give']  # "북구"
    # user = db.users.find_one({'name':'bobby'})
    # same_ages = list(db.users.find({'age':21},{'_id':False}))
    # 새로운 db에 동시에 만족하는것 추출
    # latitude_receive = request.form['latitude_give']
    # longitude_receive = request.form['longitude_give']
    # title_receive = request.form['title_give']
    # print(title_receive)
    return jsonify({'msg': '이 요청은 지도검색 POST!'})
## 지도 관련부분 버튼 끝 ##


# 메인페이지 로그인한 상태에서 동작(수정필요!)
@app.route('/mycategory', methods=['POST'])
def login_category():
    user_key = request.form['key_give']
#    print(type(user_key))
    user_data = db.login_info.find_one({'key': user_key})
    user_category = user_data["CATEGORY"]
    return jsonify({'msg': '이 요청은 로그인상태POST!', "selected_catgy": user_category})


# 새로고침 전시 기본 리스트업
@app.route('/list', methods=['GET'])
def get_list():
    exhibition_list = list(
        db.exhibition_info.aggregate([{"$sample": {"size": 20}}]))
    return jsonify({'show_list': dumps(exhibition_list)})


## 카테고리 관련부분 버튼 시작 ##

# 관심카테고리 속 다했어요 버튼 부분(수정필요!)
@app.route('/multi_s_list', methods=['POST'])
def get_selectlist():
    userdb_class = request.form['class_give']
    key_receive = request.form['key_give']

    # DB저장
    db.login_info.update_one({'key': key_receive}, {
                             '$set': {'CATEGORY': userdb_class}})
    user_name = db.login_info.find_one({"KEY": key_receive})["NAME"]
    msg = user_name + "님의 관심카테고리가 변경되었습니다."

    # 새로운 리스트정보
    selected_list = list(db.exhibition_info.aggregate(
        [{"$match": {"class": userdb_class}}, {"$sample": {"size": 20}}]))

    return jsonify({'show_list': dumps(selected_list), 'msg': msg})


# 전시 카데고리 선택 리스트업 시작
@app.route('/select_list', methods=['GET'])
def get_exhibitionlist():
    class_receive = request.args.get('class_give')
    selected_list = list(db.exhibition_info.aggregate(
        [{"$match": {"class": class_receive}}, {"$sample": {"size": 20}}]))
    return jsonify({'show_list': dumps(selected_list)})


# 상세페이지 전환
@app.route('/show_detail', methods=['POST'])
def show_detail():
   title_receive = request.form['title_give']
   target_data = db.exhibition_info.find_one({'title':title_receive}, {'_id': False})
   # userkey_receive = request.form['key_give']

   # 조회수 +1
   now_viewnm = target_data['view_num']
   new_viewnm = now_viewnm +1
   db.exhibition_info.update_one({'title':title_receive},{'$set':{'view_num':new_viewnm}})

   # # 유저 데이터에 북마크 있는지 확인
   # if userkey_receive == 'No_login':
   #     bookmark_data = 'No'
   # else:
   #     user_total_data = db.login_info.find_one({'KEY': userkey_receive}, {'_id': False})
   #     if target_data['id'] in user_total_data['BOOKMARK']:
   #         bookmark_data = 'Yes'
   #     else:
   #         bookmark_data = 'No'

   return jsonify({'target_show': target_data})
   # return jsonify({'target_show':target_data, 'bookmark_give':bookmark_data})

#######메인 관련#########

#######상세페이지#######

# @app.route('/add_bookmark', methods=['POST'])
# def add_bookmark():
#     userkey_receive = request.form['userkey_give']
#     exhibitid_receive = request.form['exhibitid_give']
#     user_total_data = db.login_info.find_one({'KEY': userkey_receive}, {'_id': False})
#     exhibit_total_data = db.exhibition_info.find_one({'id': exhibitid_receive}, {'_id': False})
#
#     if exhibit_total_data['id'] in user_total_data['BOOKMARK']:
#         # 전시회 북마크값 -1
#         bookmark_value = exhibit_total_data['bookmark_total_num']
#         new_bookmark_value = bookmark_value - 1
#         # 유저 북마크 리스트에서 제거
#         user_bookmark_list = user_total_data['BOOKMARK']
#         user_bookmark_list.remove(exhibitid_receive)
#         # DB에 업데이트
#         db.exhibition_info.update_one({'id': exhibit_total_data['id']}, {'$set': {'bookmark_total_num': new_bookmark_value}})
#         db.login_info.update_one({'KEY': userkey_receive}, {'$set': {'BOOKMARK': user_bookmark_list}})
#         # 값을 돌려줌
#         return jsonify({"Do" : "remove_complete"})
#     else:
#         # 전시회 북마크값 +1
#         bookmark_value = exhibit_total_data['bookmark_total_num']
#         new_bookmark_value = bookmark_value + 1
#         # 유저 북마크 리스트에서 제거
#         user_bookmark_list = user_total_data['BOOKMARK']
#         user_bookmark_list = user_bookmark_list + [exhibitid_receive]
#         # DB에 업데이트
#         db.exhibition_info.update_one({'id': exhibit_total_data['id']}, {'$set': {'bookmark_total_num': new_bookmark_value}})
#         db.login_info.update_one({'KEY': userkey_receive}, {'$set': {'BOOKMARK': user_bookmark_list}})
#         # 값을 돌려줌
#         return jsonify({"Do" : "add_complete"})



#######상세페이지#######



# 회원가입 api
@app.route('/sign_up', methods=['POST'])
def sign_up_post():

    session_key = ''.join(random.choice(
        string.ascii_letters + string.digits) for _ in range(8))
    # 세션키 임시로 사용 (추후 변경)

    ID_receive = request.form['ID_give']
    PASSWORD_receive = request.form['PASSWORD_give']
    NAME_receive = request.form['NAME_give']
    PHONE_NUMBER_receive = request.form['PHONE_NUMBER_give']
    CATEGORY_receive = request.form['INTEREST_CATEGORY_give']
    category_savedata = []
    if '전시' in CATEGORY_receive:
        category_savedata.append('exhibition')
    if '뮤지엄' in CATEGORY_receive:
        category_savedata.append('museum')
    if '아동체험전' in CATEGORY_receive:
        category_savedata.append('childs_experience')
    if '클래스' in CATEGORY_receive:
        category_savedata.append('class')
    if '행사/축제' in CATEGORY_receive:
        category_savedata.append('event/festival')

    doc = {

        'ID': ID_receive,
        'PASSWORD': PASSWORD_receive,
        'NAME': NAME_receive,
        'PHONE_NUMBER': PHONE_NUMBER_receive,
        'CATEGORY': category_savedata,
        'KEY': session_key,
        'BOOKMARK': []

    }
    db.login_info.insert_one(doc)
    return jsonify({'msg': 'COMPLETE'})


# 중복 확인란
@app.route('/id_overlap', methods=['POST'])
def overlap_get():
    find_ID_receive = request.form['ID_give']
    find_phone_receive = request.form['PHONE_NUMBER_give']

    same_ID = list(db.login_info.find({'ID': find_ID_receive}, {'_id': False}))
    same_PHONE = list(db.login_info.find(
        {'PHONE_NUMBER': find_phone_receive}, {'_id': False}))

    # 중복 확인 조건문

    return jsonify({'ID_result': same_ID, 'Phone_result': same_PHONE})


# 로그인 부분
# 로그인 부분
# 로그인 부분
# 로그인 부분


# db에 저장된 목록 받아오기 --> 로그인을 위해서
@app.route('/login', methods=['GET'])
def sign_up_get():
    member_list = list(db.login_info.find({}, {'_id': False}))
    return jsonify({'all_member_list': dumps(member_list)})


'''
# 회원 정보 수정

@app.route('/user_edit')
def edit_page():
    return render_template('my_info_edit.html')


# 회원 정보 조회
@app.route('/user_view', methods=['POST'])
def user_view():
    key_receive = request.form['key_give']
    user_list = list(db.login_info.find({}, {'_id': False}))
    user = user_list[int(key_receive)]
    return jsonify({'user': user})

# 회원 정보 수정 api
@app.route('/user_edit', methods=['POST'])
def user_info_edit():

    # 정보 받아오기
    my_info_receive = request.form.get('my_info_give',False)
    key_receive = request.form['key_give']

    # 바꿀 아이디 찾기
    user_list = list(db.login_info.find({}, {'_id': False}))
    user = user_list[int(key_receive)]
    user_id = user['ID']

    # 찾은 아이디에 딕셔너리를 바꾸자
    db.login_info.delete_one({'ID':user_id})
    user = my_info_receive
    db.login_info.insert_one(user)
    # db.login_info.update_one({'ID':user_id},{'$set':my_info_receive})

    user = user_list[int(key_receive)]
    return jsonify({'msg': '완료되었습니다'})

'''

# 아이디 찾기 page


@app.route('/find_id')
def Find_ID_main():
    return render_template('find_id.html')

# 아이디 찾아서 내용이 있으면, id 내용 일부를 넘김 // 내용이 없으면 없다고 넘김


@app.route('/find_id/downloadData', methods=['POST'])
def Find_ID():
    NAME_receive = request.form['NAME_give']
    # SEX_receive = request.form['SEX_give']
    PHONE_NUMBER_receive = request.form['PHONE_NUMBER_give']

    find_data = list(db.login_info.find(
        {'PHONE_NUMBER': PHONE_NUMBER_receive}, {'_id': False}))
    part_id = ""
    for id_data in find_data:
        if id_data['NAME'] == NAME_receive and id_data['PHONE_NUMBER'] == PHONE_NUMBER_receive:
            found_id = id_data['ID']
            split_front = found_id.split('@')[0]
            split_id = list(split_front)

            for i in range(len(split_id)):
                if i % 5 == 3 or i % 5 == 4:
                    split_id[i] = '*'

            part_id = "".join(split_id)
            full_id = part_id + '@' + found_id.split('@')[1]

    if not part_id == "":
        return jsonify({'id_data_find': 'find_OK', 'id_data': full_id})
    else:
        return jsonify({'id_data_find': 'find_FAIL'})

# 아이디 찾기 결과 page


@app.route('/find_id/complete')
def find_id_show():
    return render_template('find_id_complete.html')

# 비밀번호 찾기 page


@app.route('/find_pw')
def find_ps_main():
    return render_template('find_pw.html')

# 비밀번호 찾는 API


# POST 요청 (주로 DB내용을 수정,삽입 할 때 사용)
@app.route('/find_pw/downloadData', methods=['POST'])
def Find_PS():
    ID_receive = request.form['ID_give']
    NAME_receive = request.form['NAME_give']
    # SEX_receive = request.form['SEX_give']
    PHONE_NUMBER_receive = request.form['PHONE_NUMBER_give']

    cheak_change_ps = 0

    find_data = list(db.login_info.find({'ID': ID_receive}, {'_id': False}))
    for id_data in find_data:
        if id_data['NAME'] == NAME_receive and id_data['PHONE_NUMBER'] == PHONE_NUMBER_receive and id_data['ID'] == ID_receive:

            cheak_change_ps = 1

            # 새로운 비밀번호 생성
            new_password = ''.join(random.choice(
                string.ascii_letters + string.digits) for _ in range(8))
            # 새로운 비밀번호 DB에 저장
            db.login_info.update_one({'ID': id_data['ID']}, {
                                     '$set': {'PASSWORD': new_password}})

            recipients = [id_data['ID']]

            message = MIMEMultipart()
            message['Subject'] = '전시회 사이트 비밀번호 변경되었습니다.'
            message['From'] = "leegwichan@naver.com"
            message['To'] = ",".join(recipients)

            content = """
                <html>
                <body>
                    <h2>{title1}</h2>
                    <p>신규 비밀번호 : {new_ps}</p>
                    <p>로그인 하시고, 마이페이지에서 비밀번호 변경 부탁드립니다.</p>
                </body>
                </html>
            """.format(
                title1='전시회 사이트 비밀번호 변경되었습니다.',
                new_ps=new_password
            )

            mimetext = MIMEText(content, 'html')
            message.attach(mimetext)

            email_id = 'leegwichan'
            email_pw = 'mlpnkobji1'

            server = smtplib.SMTP('smtp.naver.com', 587)
            server.ehlo()
            server.starttls()
            server.login(email_id, email_pw)
            server.sendmail(message['From'], recipients, message.as_string())
            server.quit()

    if cheak_change_ps == 1:
        return jsonify({'ps_data_find': 'find_OK'})
    else:
        return jsonify({'ps_data_find': 'find_FAIL'})


# 비밀번호 찾기 결과 page
@app.route('/find_pw/complete')
def find_ps_show():
    return render_template('find_pw_complete.html')


# Mypage page
@app.route('/mypage')
def Mypage_Loadpage():
    return render_template('mypage.html')

# 마이페이지 정보 불러오기


@app.route('/mypage/basicdata', methods=['POST'])
def Mypage_load_data():
    # html 쪽에서 'sample_give'에 할당된 값을 받아옴
    userkey_receive = request.form['userkey_give']
    get_user_data = list(db.login_info.find(
        {'KEY': userkey_receive}, {'_id': False}))
    if not get_user_data:
        find_OK = 'find_fail'
        return jsonify({'Okay': find_OK})
    else:
        find_OK = 'find_success'
        user_name = get_user_data[0]['NAME']
        user_ID = get_user_data[0]['ID']
        user_phone_num = get_user_data[0]['PHONE_NUMBER']
        user_class = get_user_data[0]['CATEGORY']
        return jsonify({'Okay': find_OK,
                        'name_give': user_name,
                        'ID_give': user_ID,
                        'phone_num_give': user_phone_num,
                        'class_give': user_class})

# 마이페이지 정보 수정


@app.route('/mypage/savedata', methods=['POST'])
def Mypage_resave_data():
    key_receive = request.form['key_give']
    name_receive = request.form['name_give']
    phone_receive = request.form['phone_give']
    category_receive = []
    if request.form['exhibition_give'] == 'true':
        category_receive = category_receive + ['exhibition']
    if request.form['museum_give'] == 'true':
        category_receive = category_receive + ['museum']
    if request.form['event_give'] == 'true':
        category_receive = category_receive + ['event/festival']
    if request.form['class_give'] == 'true':
        category_receive = category_receive + ['class']
    if request.form['childs_experience_give'] == 'true':
        category_receive = category_receive + ['childs_experience']

    db.login_info.update_one({'KEY': key_receive}, {
                             '$set': {'NAME': name_receive}})
    db.login_info.update_one({'KEY': key_receive}, {
                             '$set': {'PHONE_NUMBER': phone_receive}})
    db.login_info.update_one({'KEY': key_receive}, {
                             '$set': {'CATEGORY': category_receive}})
    return jsonify({'msg': '회원정보가 저장되었습니다'})

# 마이페이지 비밀번호 수정


@app.route('/mypage/saveps', methods=['POST'])
def Mypage_resave_ps():
    key_receive = request.form['key_give']
    exist_password_receive = request.form['exist_password_give']
    new_password_receive = request.form['new_password_give']

    user_data = db.login_info.find_one({'KEY': key_receive})
    if user_data['PASSWORD'] == exist_password_receive:
        db.login_info.update_one({'KEY': key_receive}, {
                                 '$set': {'PASSWORD': new_password_receive}})
        return jsonify({'msg': 'MATCH_SUCCESS'})  # msg 라는 값으로 데이터를 넘겨줌
    else:
        return jsonify({'msg': 'MATCH_FAIL'})

# 마이페이지 회원탈퇴 기능


# POST 요청 (주로 DB내용을 수정,삽입 할 때 사용)
@app.route('/mypage/cancel_membership', methods=['POST'])
def Mypage_cancel_membership():
    key_receive = request.form['key_give']
    db.login_info.delete_one({'KEY': key_receive})
    return jsonify({'msg': '회원탈퇴가 완료되었습니다.'})  # msg 라는 값으로 데이터를 넘겨줌

# 북마크 page


@app.route('/mybookmark')
def Mybookmark_Loadpage():
    return render_template('bookmark.html')

# 북마크 페이지 데이터 불러오기


@app.route('/mybookmark/basicdata', methods=['POST'])
def write_review():
    key_receive = request.form['key_give']
    user_data = list(db.login_info.find({'KEY': key_receive}))
    if user_data:
        bookmark_data = user_data[0]['BOOKMARK']
        print(bookmark_data)
        give_exhibition_data = []
        for id_value in bookmark_data:
            exhibition_data = db.exhibition_info.find_one({'id': id_value})
            data_dict = {
                'image': exhibition_data['image_link'],
                'title': exhibition_data['title'],
                'start_date': exhibition_data['start_date'],
                'end_date': exhibition_data['end_date'],
                'place': exhibition_data['place'],
                'address_class1': exhibition_data['address_class1'],
                'address_class2': exhibition_data['address_class2']}
            give_exhibition_data = give_exhibition_data + [data_dict]
        return jsonify({'info': give_exhibition_data,
                        'Okay': 'MATCH_SUCCESS'})
    else:
        return jsonify({'Okay': 'MATCH_FAIL'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
