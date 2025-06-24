from pymongo import MongoClient
from pymongo.errors import *
from pprint import pprint
import requests
import json


'''
скачать по ссылке что-либо
'''
# response = requests.get('https://gbcdn.mrgcdn.ru/uploads/asset/5560965/attachment/357f7ccb20abaeedb8ccfda8e1045098.json')
#
# with open('crash_data.json', 'wb') as f:
#     f.write(response.content)

client = MongoClient("mongodb://admin:admin@localhost:27017")
db = client['crashes']
info = db.info

# info.delete_many({})      # снести базу
#
# with open('crash-data.json', 'r') as f:
#     data = json.load(f)
#
# count_duplicated = 0
#
# for feature in data['features']:
#     _id = feature.get('properties').get('tamainid')
#     feature['_id'] = _id
#     try:
#         info.insert_one(feature)
#     except:
#         count_duplicated += 1
#
# print(count_duplicated)

# for doc in info.find({'properties.lat2': {'$gt': 35.0, '$lt': 36.0},
#                       'properties.lon2': {'$gt': -78.0, '$lt': -77.0}}):
#     print(doc)

# for doc in info.find({'$or': [{'properties.ligthcond': 'DAYLIGHT'},
#                                {'properties.vehicle_type': 'PASSENGER CAR'}]}):
#     print(doc)


# for doc in info.find({'properties.fatality': {'$gt': 0.0}}):
#     print(doc)


# for doc in info.find({'$or': [{'properties.ligthcond': 'DARK - ROADWAY NOT LIGHTED'},
#                      {'properties.trafcontrl': 'NO CONTROL PRESENT'}],
#                      'properties.fatality': {'$gt': 0.0}}):
#     print(doc)

# for doc in info.find({
#     '$and': [
#         {
#             '$or': [
#                 {'properties.ligthcond': 'DARK - ROADWAY NOT LIGHTED'},
#                 {'properties.trafcontrl': 'NO CONTROL PRESENT'}
#             ]
#         },
#         {'properties.fatality': {'$gt': 0.0}}
#     ]
# }):
#     print(doc)

