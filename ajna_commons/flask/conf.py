import os
import pickle
import tempfile

tmpdir = tempfile.mkdtemp()

try:
    SECRET = None
    with open('SECRET', 'rb') as secret:
        try:
            SECRET = pickle.load(secret)
        except pickle.PickleError:
            pass
except FileNotFoundError:
    pass

if not SECRET:
    SECRET = os.urandom(24)
    with open('SECRET', 'wb') as out:
        pickle.dump(SECRET, out, pickle.HIGHEST_PROTOCOL)
