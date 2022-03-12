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

exhibition_list = list(db.exhibition_info.find({'place':"예술의전당 한가람디자인미술관"}))
# exhibition_list = list(db.exhibition_info.find({'place':"예술의전당 한가람디자인미술관"}).limit(20))
print(exhibition_list)