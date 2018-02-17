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


#TODO: Configure customized CSRF error 
#  http://flask.pocoo.org/docs/0.12/patterns/packages/
from flask import render_template
from flask_wtf.csrf import CSRFError

#@app.errorhandler(CSRFError)
def handle_csrf_error(e):
    return render_template('csrf_error.html', reason=e.description), 400

#TODO: Configure customized login error 
#  http://flask.pocoo.org/docs/0.12/patterns/packages/
# https://flask-login.readthedocs.io/en/latest/ - Customizing the login
#login_manager.login_view = "users.login"
#login_manager.login_message = u"Bonvolu ensaluti por uzi tiun paĝon."

