# selenium import 부분
import selenium
from selenium import webdriver
from selenium.webdriver import ActionChains

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
import time

#mongoDB 저장 패키지
from pymongo import MongoClient

client = MongoClient('localhost',27017)
db = client.exhibition_project

# 전체 데이터 불러오기
all_data = list(db.exhibition_info.find({},{'_id':False}))

# 제목 정리 (필요 없는 부분 제거)
for data in all_data:
    before_data = data['title']
    middle_data = before_data.replace('〈얼리버드 50%〉','').replace('(2022.01 ~)','').replace('［얼리버드］','').replace('［체험프로그램］','').replace('(2021년 3월 ~ 2021년 7월)','').replace('［전통주갤러리 야외정원 기념품증정］','').replace('［개인］','').replace('［단체_예약자］','').strip()
    middle2_data = middle_data.replace('［북촌］','').replace('［동탄］','').replace('［겨울특가］','').replace('［서울］','').replace('［제주］','').replace('［강릉］','').replace('［여수］','').replace('［소풍］','').replace('［할인］','').replace('［강원］','').replace('［강남］','').replace('［부산］','').strip()
    after_data = middle2_data.replace('［서울/코엑스］','').replace('［충북］','').replace('［통합권］','').replace('［파주］','').replace('(강원 춘천)','').replace('(경기도 포천)','').replace('입장권','').replace('할인 티켓','').replace('(4월티켓)','').replace('할인 티켓','').replace('할인 티켓','').replace('할인 티켓','').strip()

    # print 하여 상황 확인
    print('제목 변경: ' + before_data + '  ---------->  ' + after_data)
    db.exhibition_info.update_one({'title': data['title']}, {'$set': {'title': after_data}})

print('-----------------------------------------------------------------')

# 일부 주소 업데이트
db.exhibition_info.update_many({'place': '여수 녹테마레'}, {'$set': {'address': '전라남도 여수시 만흥동 1226'}})
db.exhibition_info.update_many({'place': '예술의전당 서예박물관'}, {'$set': {'address': '서울특별시 서초구 서초동 700'}})
db.exhibition_info.update_many({'place': '현대백화점 미아점 10층 문화홀'}, {'$set': {'address': '서울 성북구 동소문로 315'}})
db.exhibition_info.update_many({'place': '고양꽃전시관 특별전시장'}, {'$set': {'address': '경기도 고양시 일산동구 호수로 595'}})
db.exhibition_info.update_many({'place': '헤이리 아지동 플레이'}, {'$set': {'address': '경기도 파주시 탄현면 헤이리마을길 93-75'}})
db.exhibition_info.update_many({'place': 'GFX 상상놀이터'}, {'$set': {'address': '서울특별시 중구 퇴계로20길 71'}})
db.exhibition_info.update_many({'place': '군포시 평생학습원 상상극장'}, {'$set': {'address': '경기도 군포시 고산로 263'}})
db.exhibition_info.update_many({'place': '유니버설아트센터 루나홀'}, {'$set': {'address': '서울특별시 광진구 천호대로 664'}})
db.exhibition_info.update_many({'place': '남동소래아트홀 갤러리 화소'}, {'$set': {'address': '인천 남동구 아암대로1437번길 32'}})


# 수정된 전체 데이터 불러오기
all_data = list(db.exhibition_info.find({},{'_id':False}))
cheak_box = []
for data in all_data:
    # address_class1 생성
    a_address_class1 = data['address'].split(' ')[0]
    # 통일성을 맞추기 위해 OO시, OO도, OOO도, 형식으로 통일
    if a_address_class1 == '서울' or a_address_class1 == '서울특별시':
        a_address_class1 = '서울시'
    if a_address_class1 == '제주특별자치도' or a_address_class1 == '제주':
        a_address_class1 = '제주도'
    if a_address_class1 == '부산' or a_address_class1 == '부산광역시':
        a_address_class1 = '부산시'
    if a_address_class1 == '광주' or a_address_class1 == '광주광역시':
        a_address_class1 = '광주시'
    if a_address_class1 == '경기':
        a_address_class1 = '경기도'
    if a_address_class1 == '강원':
        a_address_class1 = '강원도'
    if a_address_class1 == '충북':
        a_address_class1 = '충청북도'
    if a_address_class1 == '전남':
        a_address_class1 = '전라남도'

    # address_class2 생성
    if not a_address_class1 == '온라인':
        a_address_class2 = data['address'].split(' ')[1]

    # 장소가 온라인 경우에는 class2에도 온라인으로 사용
    else:
        a_address_class2 = '온라인'

    # 해당 사항 DB 저장
    db.exhibition_info.update_many({'title': data['title']}, {'$set': {'address_class1': a_address_class1}})
    db.exhibition_info.update_many({'title': data['title']}, {'$set': {'address_class2': a_address_class2}})

    print(data['title'] + 'class 구분 저장 완료!' + a_address_class1 + ' ' + a_address_class2)

# 주소 경도 위도 크롤링

# 같은 폴더에서 크롬드라이버 불러오기
driver = webdriver.Chrome('chromedriver_window')
# 구글 지도에서 크롤링
driver.get(url='https://www.google.com/maps/')
driver.set_window_size(6000, 600)
# 해당 페이지가 전부 로드될 때 까지 대기
time.sleep(2)

# 에외 처리 리스트 값 초기 생성  (retest_place: 추출 못한 장소 모음, overlap_list: 한 번 조사한 장소 저장 -> 다시 조사하지 않음)
retest_place = []
overlap_list = []


# 수정된 데이터 다시 불러오기
all_data = list(db.exhibition_info.find({},{'_id':False}))



for data in all_data:

    time.sleep(1.5)

    # 제목 다듬어서 구글 지도 웹페이지에 넣고 검색
    before_address_data = data['address']
    middle_address_data = before_address_data.replace('(중계역 3번출구, 하계역 1번출구)','').replace('7층','').replace('섬유센터빌딩 B1','').replace('종로 아트 프라자 1, 2층','').replace('A동 지하','').replace('부산문화회관 전시실','').replace('G205','').replace('4층','').replace('지하 1, 2층 HYBE INSIGHT','').replace('A동 3층','').replace('지하 1층','').replace('(정동)','').replace('서울특별시 송파구 잠실로 209 (신천동) ','')
    middle_address_data2 = middle_address_data.replace('지상2층','').replace('1층','').replace('117~123층','').replace('(선흘리 2019-3)','').replace('(5,6번 게이트)','').replace('지하1','').replace('(황지동, 문화예술회관)','').replace('용인포은아트홀','').replace('브릭캠퍼스','').replace('브이센터','').replace('여수세계박람회 국제관 D블럭 3층','').replace('쎈토이박물관','').replace('진아트','').replace(' (삼성동) 무역센터 코엑스','').replace('(중계동)','')
    middle_address_data3 = middle_address_data2.replace('친환경식품유통센터 ','').replace('(오산동)','').replace('(신천동)','').replace('(율곡로 83)','').replace('(나운동)','').replace('(고매동)','').replace('(오산동)','').replace('(동광동3가)','').replace('(신천동)','').replace('(색달동 2629)','').replace('(광령리 100-3)','').replace('(율곡로 83)','').replace('(운양동)','').replace('지하1층','').replace('(상동)','').replace('(노형동)','').replace('(고덕동)','')
    middle_address_data4 = middle_address_data3.replace('(정동)','').replace('(정자동) 숙련기술체험관','').replace('(삼성동) 무역센터 코엑스','').replace('(신흑동)','').replace('(동숭동)','').replace('(정동)','').replace('(5,6번 게이트)','').replace('(남산동2가) 프렌쥬 그림자 상상 놀이터','').replace('(당동 871-1) 군포문화센터 5층 상상극장','').replace('(능동) 유니버설아트센터 루나홀','').strip()
    after_address_data = middle_address_data4.replace('서울특별시 송파구 잠실로 209 (신천동) ','').replace(' Ys Roo','').replace('숙련기술체험관','').replace(' 무역센터 코엑스','').replace('슈페리어타워 B','').replace('롯데백화점 동탄점','').replace('홍대 AK＆','').replace('호텔 은파팰리스','').replace('부산영화체험박물관','').replace('소인국테마파크 2층','').replace('부띠크모나코','').replace(' 구리문화재단','').replace(' 한국만화박물관','').strip()

    search_input_btn = driver.find_element(by=By.CSS_SELECTOR, value='#searchboxinput')
    search_input_btn.clear()

    if not data['address'] == '온라인':

        time.sleep(1.5)

        # 한번 조사했을 경우에는 이미 DB에 저장되어 있으므로 DB에서 데이터를 가져와 print함
        if data['address'] in overlap_list:
            download_info = db.exhibition_info.find_one({'address':data['address']},{'_id':False})
            download_latitude = download_info['latitude']
            download_longitude = download_info['longitude']
            print(data['title'] + '의 좌표 정보 이미 저장 되어있음.  ', download_latitude, download_longitude, '// 장소: ', after_address_data)

        # 조사하지 않은 데이터는 overlap_list에 추가하고 검색 실시
        if data['address'] not in overlap_list:
            overlap_list = overlap_list + [data['address']]
            search_input_btn.click()
            search_input_btn.send_keys(after_address_data)

            time.sleep(1)
            search_btn = driver.find_element(by=By.CSS_SELECTOR, value='#searchbox-searchbutton')
            search_btn.click()
            time.sleep(3)


            #검색을 했을 때, 장소가 여러개가 나오는 경우에는 추후 재조사 실시, 임시적으로 0 0 을 넣어둠
            # plus_index2는 장소가 여러개 나오는 경우 공통적인 html 부분을 나타낸 것.

            plus_index2 = driver.find_elements(by=By.XPATH, value='//*[@id="pane"]/div/div[1]/div/div/div[2]/div[1]/div[3]/div/a')

            if plus_index2:
                a_latitude = 0
                a_longitude = 0
                if data['place'] not in retest_place:
                    retest_place = retest_place + [data['place']]
                print(data['title'], '의 좌표 재조사 실시: ', a_latitude, a_longitude, '// 장소: ', data['place'])

            # 검색을 했을 때, 장소가 하나로 나오는 경우, 자료를 가져옴.
            if not plus_index2:
                # 위도: 경도 latitude & longitude 정보 google 지도의 웹페이지 주소로 가져오기
                map_url = driver.current_url
                need_data = map_url.split('/')[6].split(',')
                # 웹페이지 주소에서는 화면의 중앙의 경도,위도값이 나오기 때문에 일부 보정값을 넣어둠
                a_latitude = round(float(need_data[0].strip('@')) + 0.000062, 7)
                a_longitude = round(float(need_data[1]) + 0.002189, 7)
                print(data['title'],'의 좌표 정보: ',a_latitude , a_longitude, '// 장소: ', after_address_data)


            # 주소가 일치하는 모든 데이터에 경도,위도값을 저장
            db.exhibition_info.update_many({'address': data['address']}, {'$set': {'latitude': a_latitude}})
            db.exhibition_info.update_many({'address': data['address']}, {'$set': {'longitude': a_longitude}})



    # 주소가 온라인인 경우에는 값을 저장하지 않음
    if data['address'] == '온라인':
        print(data['title'], '은/는 온라인으로 열림')



print('재조사 할 리스트: ', retest_place)
driver.close()



# 예외 데이터 넣기 (코딩 할 수 있었으나, 머리 아파서 일일히 조사함 // 데이터가 많았다면, 제목으로 검색하는 코드를 짰을 예정)
exception_datas = [['그라운드시소 성수',37.54639029683398, 127.06523181299563],
             ['서울시립 북서울미술관',37.64080227189487, 127.06676252475017],
             ['동탄 어둠속의대화',37.201295679171814, 127.09162539386747],
             ['본다빈치뮤지엄 군산',35.95414659220776, 126.68974260783189],
             ['아이랩미디어',37.22412562655309, 127.11538235536432],
             ['양신스포츠아카데미',37.4753877309428, 127.05029721405957],
             ['에이트스퀘어 동탄',37.200620623375066, 127.09744464091074],
             ['부산 트릭아이뮤지엄＆부산영화체험박물관',35.101777681197824, 129.0336485220281],
             ['박물관은살아있다 제주',33.25491616755123, 126.40872077025071],
             ['김포아트빌리지 아트센터',37.645459219951015, 126.6959449941292],
             ['한국만화박물관(부천)',37.50873928342257, 126.74223097121121],
             ['쎈토이박물관',37.24465143147491, 127.61577143317491],
             ['여주곤충박물관',37.29802515025683, 127.63716492523533],
             ['코버월드',37.8994940869773, 127.21341800839232],
             ['브릭캠퍼스',33.45840665500307, 126.48546720223197],
             ['세계술박물관',33.35395416863774, 126.81770868290214],
             ['제주공룡동물농장',33.40667628695956, 126.84489956147286],
             ['북촌 어둠속의대화',37.5832975170162, 126.98482936377448],
            ['타임워크 명동 1층',37.56420650772611, 126.98288573632772],
            ['군포문화예술회관 제1전시실, 제2전시실',37.36612854753956, 126.92732027323426],
            ['피규어뮤지엄W',37.525759120430614, 127.04038381061265],
            ['갤러리아포레',37.54570328495779, 127.04242207033414]]




for data in exception_datas:

    # 데이터 베이스에 저장 / 장소가 동일한 모든 데이터에 같은 경도,위도 값을 저장
    db.exhibition_info.update_many({'place': data[0]}, {'$set': {'latitude': data[1]}})
    db.exhibition_info.update_many({'place': data[0]}, {'$set': {'longitude': data[2]}})
    print('예외 좌표정보 추가: ' + data[0] + '//' + str(data[1]) + ', '+ str(data[2]))


missing_place_data = list(db.exhibition_info.find({'longitude':0},{'_id':False}))
for missing_data in missing_place_data:
    print('누락된 데이터: ',missing_data['place'],'//',missing_data['title'])
