from pymongo import MongoClient

client = MongoClient('3.91.50.100',27017,
                     username='noE',
                     password='server_test')
db = client.exhibition_project

total_data = list(db.exhibition_info.find({},{'_id':False}))
print('AWS에서 데이터 전부 불러옴')


client = MongoClient('localhost',27017)
db = client.exhibition_project

for data in total_data:
    db.exhibition_info.insert_one(data)
    print(data['title'],': local DB에 업데이트 됨')




client = MongoClient('3.91.50.100',27017,
                     username='noE',
                     password='server_test')
db = client.exhibition_project

total_data2 = list(db.region_info.find({},{'_id':False}))
print('AWS에서 데이터 전부 불러옴')


client = MongoClient('localhost',27017)
db = client.exhibition_project

for data2 in total_data2:
    db.region_info.insert_one(data2)
    print(data2['address_class2'],': local DB에 업데이트 됨')