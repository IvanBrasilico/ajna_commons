"""Define configurações comuns aos módulos do AJNA
Ex.:
SECRET - chave para criptografia da sessão
REDIS SERVER
MONGODB SERVER
Custom messages- mensagens customizadas para módulos de login, segurança,
 erro, etc
Configurações de logging, etc
"""
# import logging
import os
import pickle
import redis
import tempfile
# from ajna_commons.flask.log import logger
from dominate.tags import img

tmpdir = tempfile.mkdtemp()
logo = img(src='/static/css/images/logo.png')

try:
    with open('SECRET', 'rb') as secret:
        try:
            SECRET = pickle.load(secret)
        except pickle.PickleError:
            SECRET = None
except FileNotFoundError:
    SECRET = None

if SECRET is None:
    SECRET = os.urandom(24)
    with open('SECRET', 'wb') as out:
        pickle.dump(SECRET, out, pickle.HIGHEST_PROTOCOL)


BSON_REDIS = 'bson'
REDIS_URL = os.environ.get('REDIS_URL')
if not REDIS_URL:
    REDIS_URL = 'redis://localhost:6379'
BACKEND = BROKER = REDIS_URL
redisdb = redis.StrictRedis.from_url(REDIS_URL)

MONGODB_URI = os.environ.get('MONGODB_URI')
if MONGODB_URI:
    DATABASE = ''.join(MONGODB_URI.rsplit('/')[-1:])
    # print(DATABASE)
else:
    DATABASE = 'test'


SENTRY_DSN = os.environ.get('SENTRY_DSN')


# initialize constants used for server queuing
TIMEOUT = 10
BATCH_SIZE = 1000
ALLOWED_EXTENSIONS = set(['csv', 'zip', 'txt', 'png', 'jpg', 'jpeg', 'sch'])
