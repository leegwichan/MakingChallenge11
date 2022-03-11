from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

from pymongo import MongoClient

client = MongoClient('mongodb://noE:server_test@localhost', 27017)
db = client.dbsparta

import requests
import re



# 각 html에 맞는 route가 있으니 필요에 따라 주석 제거하면서 실행해 보시면 됩니다!




# 회원가입 부분
# 회원가입 부분
# 회원가입 부분
# 회원가입 부분



# html 받아오는 부분
@app.route('/')
def home():
    return render_template('join.html')

@app.route('/main')
def main():
    return render_template('main.html')

# api

# 회원가입
@app.route('/sign_up', methods=['POST'])
def sign_up_post():

    session_key = ''

    ID_receive = request.form['ID_give']
    PASSWORD_receive = request.form['PASSWORD_give']
    NAME_receive = request.form['NAME_give']
    PHONE_NUMBER_receive = request.form['PHONE_NUMBER_give']
    CATEGORY_receive = request.form['INTEREST_CATEGORY_give']

    # 아이디의 아스키 코드를 key 값으로 설정
    len_id = len(ID_receive)
    for i in range(len_id):
        session_key += str(ord(str((ID_receive[i]))))

    doc = {

        'ID': ID_receive,
        'PASSWORD': PASSWORD_receive,
        'NAME': NAME_receive,
        'PHONE_NUMBER': PHONE_NUMBER_receive,
        'CATEGORY': CATEGORY_receive,
        'KEY' : session_key

    }
    db.login_info.insert_one(doc)
    return jsonify({'msg': 'COMPLETE'})




# 중복 확인란
@app.route('/id_overlap', methods=['POST'])
def overlap_get():
    find_ID_receive = request.form['ID_give']
    find_phone_receive = request.form['PHONE_NUMBER_give']

    same_ID = list(db.login_info.find({'ID': find_ID_receive},{'_id':False}))
    same_PHONE = list(db.login_info.find({'PHONE_NUMBER': find_phone_receive},{'_id':False}))

    # 중복 확인 조건문


    return jsonify({'ID_result':same_ID, 'Phone_result':same_PHONE})




# 로그인 부분
# 로그인 부분
# 로그인 부분
# 로그인 부분

@app.route('/login_page')
def login_page():
    return render_template('login.html')


# db에 저장된 목록 받아오기 --> 로그인을 위해서
@app.route('/login', methods=['GET'])
def sign_up_get():
    member_list = list(db.login_info.find({}, {'_id': False}))
    return jsonify({'all_member_list': member_list})



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




if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
