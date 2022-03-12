#Flask 사용하기 전에 해야할 일들


# 기본 세팅(Flask)
from flask import Flask, render_template, jsonify, request
app = Flask(__name__)
#기본 세팅(MongoDB)
from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.exhibition_project



## HTML을 주는 부분
@app.route('/')
def home():
    return render_template('main.html')     #template 파필에 있는 'main.html'을 불러옴

# Mypage page
@app.route('/mypage')
def Mypage_Loadpage():
    return render_template('mypage.html')

@app.route('/mypage/basicdata', methods=['POST'])     # POST 요청 (주로 DB내용을 수정,삽입 할 때 사용)
def Mypage_load_data():
    userkey_receive = request.form['userkey_give']  # html 쪽에서 'sample_give'에 할당된 값을 받아옴
    get_user_data = list(db.login_info.find({'KEY':userkey_receive},{'_id':False}))
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
                    'phone_num_give' : user_phone_num,
                    'class_give' : user_class})

@app.route('/mypage/savedata', methods=['POST'])     # POST 요청 (주로 DB내용을 수정,삽입 할 때 사용)
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
    if request.form['childs_experience_give'] =='true':
        category_receive = category_receive + ['childs_experience']


    db.login_info.update_one({'KEY': key_receive}, {'$set': {'NAME': name_receive}})
    db.login_info.update_one({'KEY': key_receive}, {'$set': {'PHONE_NUMBER': phone_receive}})
    db.login_info.update_one({'KEY': key_receive}, {'$set': {'CATEGORY': category_receive}})
    return jsonify({'msg': '회원정보가 저장되었습니다'})     # msg 라는 값으로 데이터를 넘겨줌

@app.route('/mypage/saveps', methods=['POST'])     # POST 요청 (주로 DB내용을 수정,삽입 할 때 사용)
def Mypage_resave_ps():
    key_receive = request.form['key_give']
    exist_password_receive = request.form['exist_password_give']
    new_password_receive = request.form['new_password_give']

    user_data = db.login_info.find_one({'KEY': key_receive})
    if user_data['PASSWORD'] == exist_password_receive:
        db.login_info.update_one({'KEY': key_receive}, {'$set': {'PASSWORD': new_password_receive}})
        return jsonify({'msg': 'MATCH_SUCCESS'})     # msg 라는 값으로 데이터를 넘겨줌
    else:
        return jsonify({'msg': 'MATCH_FAIL'})

@app.route('/mypage/cancel_membership', methods=['POST'])     # POST 요청 (주로 DB내용을 수정,삽입 할 때 사용)
def Mypage_cancel_membership():
    key_receive = request.form['key_give']
    db.users.delete_one({'KEY': key_receive})
    return jsonify({'msg': '회원탈퇴가 완료되었습니다.'})     # msg 라는 값으로 데이터를 넘겨줌

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
        give_exhibition_data = []
        for id_value in bookmark_data:
            exhibition_data = db.exhibition_info.find_one({'_id': id_value})
            data_dict = {
                'image': exhibition_data['image_link'],
                'title': exhibition_data['title'],
                'start_date': exhibition_data['start_date'],
                'end_date': exhibition_data['end_date'],
                'place': exhibition_data['place']}
            give_exhibition_data = give_exhibition_data + [data_dict]

        return jsonify({'info': give_exhibition_data,
                        'Okay': 'MATCH_SUCCESS'})
    else:
        return jsonify({'Okay': 'MATCH_FAIL'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)