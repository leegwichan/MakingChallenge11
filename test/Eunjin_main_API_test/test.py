from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

#지도 관련

import folium
from geopy.geocoders import Nominatim
from collections import Counter

from pymongo import MongoClient
client = MongoClient('18.208.182.249',27017,
                     username='noE',
                     password='server_test')
db = client.exhibition_project

# data = db.exhibition_info.aggregate([{"$sample":{ "size": 20}}])
# print(type(data)) #<class 'pymongo.command_cursor.CommandCursor'>
# data = db.exhibition_info.find()
# print(type(data)) #<class 'pymongo.cursor.Cursor'>

# exhibition_list = list(db.exhibition_info.aggregate([{"$sample":{ "size": 20}}]))

# for i in exhibition_list:
#     print(i)
#     print(exhibition_list.index(i))
#     print("--------")


# in은 특정 key의 값이 ㅁㅁㅁ인 경우에 사용한다.
# db.nettuts.find( { 'occupation' : { '$in' : [ "actor", "developer" ] } }, { "first" : 1, "last" : 1 } );
# 출처: https://fors.tistory.com/403 [Code]

# class_receive = "exhibition"
# exhibition_list = list(db.exhibition_info.aggregate([{"$match": { "class": class_receive }},{"$sample":{ "size": 20}}]))
# for i in exhibition_list:
#     print(i)
#     print(exhibition_list.index(i))
#     print("--------")

title_receive = "숙련기술체험관(만11~18세)"
target_data = db.exhibition_info.find_one({'title':title_receive}, {'_id': False})
print(target_data['view_num'])
# now_viewn= target_data['view_num']
# print(type(now_viewn))


