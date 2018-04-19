"""Teste de funcionalidade do MongoDB."""
import os

from pymongo import MongoClient

MONGODB_URI = os.environ.get('MONGODB_URI')
if MONGODB_URI:
    DATABASE = ''.join(MONGODB_URI.rsplit('/')[-1:])
    print(DATABASE)
else:
    DATABASE = 'test'

db = MongoClient(host=MONGODB_URI)[DATABASE]


user = db.users.find_one({'username': 'ivan', 'password': 'ivan'})

if user is None:
    db.users.insert({'username': 'ivan', 'password': 'ivan'})
