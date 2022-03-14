from pymongo import MongoClient

client = MongoClient('18.208.182.249',27017,
                     username='noE',
                     password='server_test')
# client = MongoClient('localhost',27017)
db = client.exhibition_project



list = list(db.exhibition_info.find())

for x in range(len(list)):
    id_value = list[x]['_id']
    if 0<x+1<10:
        a_id = '0000000' + str(x+1)
    elif 10<=x+1<100:
        a_id = '000000' + str(x+1)
    elif 100<=x+1<1000:
        a_id = '00000' + str(x+1)
    elif 1000<=x+1<10000:
        a_id = '0000' + str(x+1)
    else:
        a_id = str(x+1)

    db.exhibition_info.update_one({'_id':id_value}, {'$set': {'id': a_id}})
    print('id값 부여완료:  ',a_id)



