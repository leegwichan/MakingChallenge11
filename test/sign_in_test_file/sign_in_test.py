from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.dbsparta


# 회원가입 부분
'''
html 받아오는 부분
@app.route('/')
def home():
    return render_template('API_TEST.html')

# api

# 회원가입
@app.route('/login', methods=['POST'])
def sign_up_post():
    ID_receive = request.form['ID_give']
    PASSWORD_receive = request.form['PASSWORD_give']
    NAME_receive = request.form['NAME_give']
    SEX_receive = request.form['SEX_give']
    RRN_receive = request.form['RRN_give']
    PHONE_NUMBER_receive = request.form['PHONE_NUMBER_give']
    E_MAIL_receive = request.form['E_MAIL_give']
    LOCATION_receive = request.form['LOCATION_give']
    # BOOKMARK_receive = request.form['BOOKMARK_give']

    doc = {
        'ID': ID_receive,
        'PASSWORD': PASSWORD_receive,
        'NAME': NAME_receive,
        'SEX': SEX_receive,
        'RRN': RRN_receive,
        'PHONE_NUMBER': PHONE_NUMBER_receive,
        'E_MAIL': E_MAIL_receive,
        'LOCATION': LOCATION_receive,
        # 'BOOKMARK': BOOKMARK_receive
    }
    db.login_info.insert_one(doc)
    return jsonify({'msg': 'COMPLETE'})




# 중복 확인란
@app.route('/id_overlap', methods=['POST'])
def overlap_get():
    find_id_receive = request.form['find_id_give']
    find_phone_receive = request.form['find_phone_give']
    find_email_receive = request.form['find_email_give']
    find_RRN_receive = request.form['find_RRN_give']


    same_ID = db.login_info.find({'ID': find_id_receive},{'_id':False})
    same_PHONE = db.login_info.find({'E_MAIL': find_phone_receive},{'_id':False})
    same_E_MAIL = db.login_info.find({'E_MAIL': find_email_receive},{'_id':False})
    same_RRN = db.login_info.find({'RRN': find_RRN_receive},{'_id':False})

    # 중복 확인 조건문
    if same_ID is not None:
        ID_result = '아이디가 중복됩니다'
    else:
        ID_result = ''
    if same_PHONE is not None:
        Phone_result = '같은 전화번호가 존재합니다'
    else:
        Phone_result = ''
    if same_E_MAIL is not None:
        E_mail_result = '해당 이메일 계정이 존재합니다'
    else:
        E_mail_result = ''
    if same_RRN is not None:
        RRN_result = '이미 계정이 존재합니다(주민번호)'
    else:
        RRN_result = ''

    return jsonify({'ID_result':ID_result, 'Phone_result':Phone_result, 'E_mail_result':E_mail_result, 'RRN_result': RRN_result})

'''

# 로그인 부분
@app.route('/')
def main():
    return render_template('login.html')


# db에 저장된 목록 받아오기 --> 로그인을 위해서
@app.route('/login', methods=['GET'])
def sign_up_get():
    member_list = list(db.login_info.find({}, {'_id': False}))
    return jsonify({'all_member_list': member_list})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
