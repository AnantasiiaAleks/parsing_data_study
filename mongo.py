from pymongo import MongoClient
from pymongo.errors import *
from pprint import pprint

# client = MongoClient('localhost', 27017)

client = MongoClient("mongodb://admin:admin@localhost:27017")

# Проверка подключения
# print(client.list_database_names())
db = client['users']
# db2 = client['books']
persons = db.persons
duplicates = db.duplicates


# doc = {
#     "_id": "123asd",
#     "autor": "Peter",
#     "age": 38,
#     "text": "It's cool! Wildberry",
#     "tags": ['cool', 'hot', 'Ice'],
#     "date": '14.06.1983'
# }
#
# try:
#     persons.insert_one(doc)
# except DuplicateKeyError as e:
#     print(e)


# authors_list = [
#     {
#         "author": "John",
#         "age": 29,
#         "text": "Too bad! Strawberry",
#         "tags": "Ice",
#         "date": '04.08.1971'
#     },
#     {
#         "_id": 123,
#         "author": "Anna",
#         "age": 36,
#         "title": "Hot Cool!!!",
#         "text": "easy too",
#         "date": '26.01.1995'
#     },
#     {
#         "author": "Jane",
#         "age": 43,
#         "title": "Nice book!",
#         "text": "Pretty text not long",
#         "date": '08.08.1975',
#         "tags": ['fantastic', 'original']
#     }
# ]
#
# # persons.insert_many(authors_list)   # может поломать БД, лучше итерироваться по списку и использовать insert_one
# for author in authors_list:
#     try:
#         persons.insert_one(author)
#     except DuplicateKeyError as e:
#         duplicates.insert_one(author)
#
# for doc in persons.find():
#     print()
#     pprint(doc)
#
# for dup in duplicates.find():
#     pprint(dup)



# for doc in persons.find({'autor':'Peter', 'age': 38}):  # логическое И
#     print(doc)

# for doc in persons.find({'$or': [{'autor': 'Peter'}, {'age': 29}]}):   # логическое ИЛИ
#     print(doc)

# for doc in persons.find({'age': {'$gt': 40}}):   # больше, чем...
#     print(doc)

# for doc in persons.find({'author': {'$regex': 'J.'}}):   # регулярное выражение regex
#     print(doc)

# for doc in persons.find({'author': {'$regex': 'J.'}}, {'_id': 0}):   # -||- вывод без поля _id
#     print(doc)

# for doc in persons.find({'author': {'$regex': 'J.'}}, {'_id': 0}).sort('age'):   # -||- с сортировкой по полю age
#     print(doc)

# for doc in persons.find({'author': {'$regex': 'J.'}}, {'_id': 0}).sort('age', -1):   # -||- с сортировкой по полю age по убыванию
#     print(doc)

# persons.update_one({'autor': 'Peter'}, {'$set': {'autor': 'Vasya'}})   # обновление записи (добавление записи, если менять ключ

new_data = {
    "autor": "Andrey",
    "age": 28,
    "text": "Is hot",
    "date": '28.01.1998'
}

new_peter = {
    "author": "Stepan",
    "age": 33,
    "text": "Hi, I was Peter",
    "date": '12.06.2025'
}

# persons.update_one({'autor': 'Peter'}, {'$set': new_data})      # обновление из переменной

# persons.replace_one({'autor': 'Peter'}, new_peter) # замена всей "строки" на новую"

persons.delete_one({'autor': 'Peter'})  # удаление записи

for doc in persons.find():
    print(doc)