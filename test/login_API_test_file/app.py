from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.dbsparta


# html 받아오는 부분
@app.route('/')
def home():
    return render_template('index.html')


# api
@app.route('/login_info', methods=['POST'])
def sign_up_post():
    ID_receive = request.form['ID_give']
    PASSWORD_receive = request.form['PASSWORD_give']
    NAME_receive = request.form['NAME_give']
    SEX_receive = request.form['SEX_give']
    RRN_receive = request.form['RRN_receive']
    PHONE_NUMBER_receive = request.form['PHONE_NUMBER_give']
    E_MAIL_receive = request.form['E_MAIL_give']
    LOCATION_receive = request.form['LOCATION_give']
    BOOKMARK_receive = request.form['BOOKMARK_give']


    # 중복된 ID, 주민번호, e-mail이 있는지 확인하기 위해 변수 초기화
    same_ID = list(db.login_info.find({'ID': ID_receive}))
    same_RRN = list(db.login_info.find({'RRN': RRN_receive}))
    same_E_MAIL = list(db.login_info.find({'E_MAIL': E_MAIL_receive}))

    # 중복 된 것이 없다면 insert, 있다면 alert를 위해 msg에 경고문 띄움
    if same_RRN is not None:
        if same_ID is not None:
            if same_E_MAIL is not None:

                doc = {
                    'ID': ID_receive,
                    'PASSWORD': PASSWORD_receive,
                    'NAME': NAME_receive,
                    'SEX': SEX_receive,
                    'RRN': RRN_receive,
                    'PHONE_NUMBER': PHONE_NUMBER_receive,
                    'E_MAIL': E_MAIL_receive,
                    'LOCATION': LOCATION_receive,
                    'BOOKMARK': BOOKMARK_receive
                }
                db.login_info.insert_one(doc)
                return jsonify({'msg': 'COMPLETE'})

            else: return jsonify({'msg': '중복된 e-mail이 존재합니다.' })
        else: return jsonify({'msg': '중복된 ID가 존재합니다.' })
    else: return jsonify({'msg': '중복된 주민등록번호가 존재합니다.' })






# mongodb에 저장된 data들을 get 해온것, all_member_list에 저장했습니다.
@app.route('/login_info', methods=['GET'])
def sign_up_get():
    member_list = list(db.login_info.find({}, {'_id': False}))
    return jsonify({'all_member_list': member_list})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
