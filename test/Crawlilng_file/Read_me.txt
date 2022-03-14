Interpark_Crawling, Interpark_Crawling2, Interpark_Crawling3_Addinfo
순서대로 3가지 돌리면 직접 크롤링 가능

Downlod_AWSdb 실행시키시면 AWS에 있는 데이터 받아오실 수 있습니다.



후자로 돌리시는 것을 추천
---------------------------------------------
from pymongo import MongoClient

client = MongoClient('localhost',27017)
db = client.exhibition_project
--------------------------------------------
collection이름은 exhibition_info 로 사용



Position_Crawling은 직접 돌리지 않는 것을 추천함.
Update_id_vlaue : 전시회 정보값에 id 부여.