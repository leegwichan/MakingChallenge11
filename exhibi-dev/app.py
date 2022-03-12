# flask import
from flask import Flask, render_template, jsonify, request
app = Flask(__name__)
#pymongo import
from pymongo import MongoClient
client = MongoClient('18.208.182.249',27017,
                     username='noE',
                     password='server_test')
db = client.exhibition_project
# random 관련 import
import string
import random

# password 찾기 관련 import
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


@app.route('/')
def home():
    return render_template('main.html')

# html 받아오는 부분 # 회원가입 부분
@app.route('/join')
def join_Loadpage():
    return render_template('join.html')


# 회원가입 api
@app.route('/sign_up', methods=['POST'])
def sign_up_post():

    session_key = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(8))
    ## 세션키 임시로 사용 (추후 변경)

    ID_receive = request.form['ID_give']
    PASSWORD_receive = request.form['PASSWORD_give']
    NAME_receive = request.form['NAME_give']
    PHONE_NUMBER_receive = request.form['PHONE_NUMBER_give']
    CATEGORY_receive = request.form['INTEREST_CATEGORY_give']
    category_savedata = []
    if '전시' in CATEGORY_receive:
        category_savedata = category_savedata + 'exhibition'
    if '뮤지엄' in CATEGORY_receive:
        category_savedata = category_savedata + 'museum'
    if '아동체험전' in CATEGORY_receive:
        category_savedata = category_savedata + 'childs_experience'
    if '클래스' in CATEGORY_receive:
        category_savedata = category_savedata + 'class'
    if '행사/축제' in CATEGORY_receive:
        category_savedata = category_savedata + 'event/festival'

    doc = {

        'ID': ID_receive,
        'PASSWORD': PASSWORD_receive,
        'NAME': NAME_receive,
        'PHONE_NUMBER': PHONE_NUMBER_receive,
        'CATEGORY': CATEGORY_receive,
        'KEY' : category_savedata

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
    SEX_receive = request.form['SEX_give']
    PHONE_NUMBER_receive = request.form['PHONE_NUMBER_give']

    find_data = list(db.login_info.find({'PHONE_NUMBER': PHONE_NUMBER_receive}, {'_id': False}))
    part_id = ""
    for id_data in find_data:
        if id_data['NAME'] == NAME_receive and id_data['SEX'] == SEX_receive and id_data['PHONE_NUMBER'] == PHONE_NUMBER_receive:
            found_id = id_data['ID']
            split_front = found_id.split('@')[0]
            split_id = list(split_front)

            for i  in range(len(split_id)):
                if  i % 5 == 3 or i % 5 == 4:
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
@app.route('/find_ps/downloadData', methods=['POST'])     # POST 요청 (주로 DB내용을 수정,삽입 할 때 사용)
def Find_PS():
    ID_receive = request.form['ID_give']
    NAME_receive = request.form['NAME_give']
    SEX_receive = request.form['SEX_give']
    PHONE_NUMBER_receive = request.form['PHONE_NUMBER_give']

    cheak_change_ps = 0

    find_data = list(db.login_info.find({'ID': ID_receive}, {'_id': False}))
    for id_data in find_data:
        if id_data['NAME'] == NAME_receive and id_data['SEX'] == SEX_receive and id_data['PHONE_NUMBER'] == PHONE_NUMBER_receive and id_data['ID'] == ID_receive:

            cheak_change_ps = 1

            # 새로운 비밀번호 생성
            new_password = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(8))
            # 새로운 비밀번호 DB에 저장
            db.login_info.update_one({'ID': id_data['ID']}, {'$set': {'PASSWORD': new_password}})

            recipients = [id_data['ID']]

            message = MIMEMultipart();
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
                new_ps = new_password
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

#마이페이지 정보 불러오기
@app.route('/mypage/basicdata', methods=['POST'])
def Mypage_load_data():
    userkey_receive = request.form['userkey_give']  # html 쪽에서 'sample_give'에 할당된 값을 받아옴
    get_user_data = list(db.login_info.find({'KEY': userkey_receive}, {'_id': False}))
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

    db.login_info.update_one({'KEY': key_receive}, {'$set': {'NAME': name_receive}})
    db.login_info.update_one({'KEY': key_receive}, {'$set': {'PHONE_NUMBER': phone_receive}})
    db.login_info.update_one({'KEY': key_receive}, {'$set': {'CATEGORY': category_receive}})
    return jsonify({'msg': '회원정보가 저장되었습니다'})

# 마이페이지 비밀번호 수정
@app.route('/mypage/saveps', methods=['POST'])
def Mypage_resave_ps():
    key_receive = request.form['key_give']
    exist_password_receive = request.form['exist_password_give']
    new_password_receive = request.form['new_password_give']

    user_data = db.login_info.find_one({'KEY': key_receive})
    if user_data['PASSWORD'] == exist_password_receive:
        db.login_info.update_one({'KEY': key_receive}, {'$set': {'PASSWORD': new_password_receive}})
        return jsonify({'msg': 'MATCH_SUCCESS'})  # msg 라는 값으로 데이터를 넘겨줌
    else:
        return jsonify({'msg': 'MATCH_FAIL'})

# 마이페이지 회원탈퇴 기능
@app.route('/mypage/cancel_membership', methods=['POST'])  # POST 요청 (주로 DB내용을 수정,삽입 할 때 사용)
def Mypage_cancel_membership():
    key_receive = request.form['key_give']
    db.users.delete_one({'KEY': key_receive})
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
