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

# 같은 폴더에서 크롬드라이버 불러오기
driver = webdriver.Chrome('chromedriver_window')
# 인터파크 전시회 검색결과 띄우기 // 현재 여러분야 중 전시 분야만 크롤링함
driver.get(url='https://www.google.com/maps/')
# 해당 페이지가 전부 로드될 때 까지 대기
time.sleep(1.5)

search_input_btn = driver.find_element(by=By.CSS_SELECTOR, value='#searchboxinput')
search_btn = driver.find_element(by=By.CSS_SELECTOR, value='#searchbox-searchbutton')

area0 = ["서울시", "인천시", "대전시", "광주시", "대구시", "울산시", "부산시", "경기도", "강원도", "충청북도", "충청남도", "전라북도", "전라남도", "경상북도", "경상남도", "제주도"];
area1 = ["강남구", "강동구", "강북구", "강서구", "관악구", "광진구", "구로구", "금천구", "노원구", "도봉구", "동대문구", "동작구", "마포구", "서대문구", "서초구", "성동구", "성북구", "송파구", "양천구", "영등포구", "용산구", "은평구", "종로구", "중구", "중랑구"];
area2 = ["계양구", "남구", "남동구", "동구", "부평구", "서구", "연수구", "중구", "강화군", "옹진군"];
area3 = ["대덕구", "동구", "서구", "유성구", "중구"];
area4 = ["광산구", "남구", "동구", "북구", "서구"];
area5 = ["남구", "달서구", "동구", "북구", "서구", "수성구", "중구", "달성군"];
area6 = ["남구", "동구", "북구", "중구", "울주군"];
area7 = ["강서구", "금정구", "남구", "동구", "동래구", "부산진구", "북구", "사상구", "사하구", "서구", "수영구", "연제구", "영도구", "중구", "해운대구", "기장군"];
area8 = ["고양시", "과천시", "광명시", "광주시", "구리시", "군포시", "김포시", "남양주시", "동두천시", "부천시", "성남시", "수원시", "시흥시", "안산시", "안성시", "안양시", "양주시", "오산시", "용인시", "의왕시", "의정부시", "이천시", "파주시", "평택시", "포천시", "하남시", "화성시", "가평군", "양평군", "여주군", "연천군"];
area9 = ["강릉시", "동해시", "삼척시", "속초시", "원주시", "춘천시", "태백시", "고성군", "양구군", "양양군", "영월군", "인제군", "정선군", "철원군", "평창군", "홍천군", "화천군", "횡성군"];
area10 = ["제천시", "청주시", "충주시", "괴산군", "단양군", "보은군", "영동군", "옥천군", "음성군", "증평군", "진천군", "청원군"];
area11 = ["계룡시", "공주시", "논산시", "보령시", "서산시", "아산시", "천안시", "금산군", "당진군", "부여군", "서천군", "연기군", "예산군", "청양군", "태안군", "홍성군"];
area12 = ["군산시", "김제시", "남원시", "익산시", "전주시", "정읍시", "고창군", "무주군", "부안군", "순창군", "완주군", "임실군", "장수군", "진안군"];
area13 = ["광양시", "나주시", "목포시", "순천시", "여수시", "강진군", "고흥군", "곡성군", "구례군", "담양군", "무안군", "보성군", "신안군", "영광군", "영암군", "완도군", "장성군", "장흥군", "진도군", "함평군", "해남군", "화순군"];
area14 = ["경산시", "경주시", "구미시", "김천시", "문경시", "상주시", "안동시", "영주시", "영천시", "포항시", "고령군", "군위군", "봉화군", "성주군", "영덕군", "영양군", "예천군", "울릉군", "울진군", "의성군", "청도군", "청송군", "칠곡군"];
area15 = ["거제시", "김해시", "마산시", "밀양시", "사천시", "양산시", "진주시", "진해시", "창원시", "통영시", "거창군", "고성군", "남해군", "산청군", "의령군", "창녕군", "하동군", "함안군", "함양군", "합천군"];
area16 = ["서귀포시", "제주시", "남제주군", "북제주군"];
area_list = [ area1,area2,area3,area4,area5,area6,area7,area8,area9,area10,area11,area12,area13,area14,area15,area16]


revise_data_cheak = ['14z', '13z', '12z', '15z']
revise_data = [0.018383565987477368, 0.11513773894324686, 0.09110639616510241, 0.14874267460098167]

for x in range(len(area0)):
    class1 = area0[x]
    for class2 in area_list[x]:
        search_input_btn.clear()
        time.sleep(1)
        search_text = class1 + " " + class2

        search_input_btn.click()
        time.sleep(0.5)
        search_input_btn.send_keys(search_text)
        time.sleep(0.5)
        search_btn.click()
        time.sleep(1.5)

        # 위도: 경도 latitude & longitude 정보 google 지도의 웹페이지 주소로 가져오기
        map_url = driver.current_url
        need_data = map_url.split('/')[6].split(',')
        # 웹페이지 주소에서는 화면의 중앙의 경도,위도값이 나오기 때문에 일부 보정값을 넣어둠
        url_latitude = need_data[0].strip('@')
        url_longitude = need_data[1]
        url_zoom = need_data[2]


        if url_zoom not in revise_data_cheak:
            real_data = input("실제 위치를 입력하세요.")
            a_latitude = round(float(url_latitude),7)
            a_longitude = round(float(real_data.split(',')[1]),7)
            print(a_longitude)

            re = float(real_data.split(',')[1]) - float(url_longitude)
            revise_data_cheak = revise_data_cheak + [url_zoom]
            revise_data = revise_data + [re]
            print(revise_data_cheak)
            print(revise_data)
        else:
            a_latitude = round(float(url_latitude),7)
            a_longitude = round(float(url_longitude) - revise_data[revise_data_cheak.index(url_zoom)],7)

        doc = {
            'address_class1': class1,
            'address_class2': class2,
            'latitude': a_latitude,
            'longitude': a_longitude
        }

        print(doc)
        db.region_info.insert_one(doc)