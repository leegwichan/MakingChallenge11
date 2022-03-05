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
db = client.exhibition_info

# 같은 폴더에서 크롬드라이버 불러오기
driver = webdriver.Chrome('chromedriver_window')
# 네이버 전시회 검색결과 띄우기
driver.get(url='http://ticket.interpark.com/TPGoodsList.asp?Ca=Eve&SubCa=Eve_O&tid4=Eve_O')
# 해당 페이지가 전부 로드될 때 까지 대기
time.sleep(2)

divs = driver.find_elements(by=By.CSS_SELECTOR, value='body > table > tbody > tr:nth-child(2) > td:nth-child(3) > div > div > div.con > div > table > tbody > tr')
for div in divs:
    a_title = div.find_element(by=By.CSS_SELECTOR, value='td.RKtxt > span > a').text
    a_ticket_link = div.find_element(by=By.CSS_SELECTOR, value='td.RKtxt > span > a').get_attribute("href")
    a_image_link = div.find_element(by=By.CSS_SELECTOR, value='td.RKthumb > a > img').get_attribute("src")
    a_place = div.find_element(by=By.CSS_SELECTOR, value='td:nth-child(3) > a').text
    a_place_link = div.find_element(by=By.CSS_SELECTOR, value='td:nth-child(3) > a').get_attribute("href")
    a_start_date = div.find_element(by=By.CSS_SELECTOR, value='td:nth-child(4)').text
    # print(a_title, a_ticket_link, a_image_link, a_place, a_place_link, a_start_date)
    # 전시회 정보 mongoDB에 저장
    doc = {
        'title': a_title,
        'ticket_link': a_ticket_link,
        'image_link': a_image_link,
        'place': a_place,
        'place_link': a_place_link,
        'start_date': a_start_date
    }
    db.exhibition_info.insert_one(doc)
driver.close()
