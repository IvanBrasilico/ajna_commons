# Tescases for virasana.app.py
import unittest

from flask import Flask, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_nav import Nav
from flask_nav.elements import Navbar, View
from flask_login import current_user
from pymongo import MongoClient
from ajna_commons.flask.conf import MONGODB_URI

import ajna_commons.flask.login as login


class FlaskTestCase(unittest.TestCase):
    def setUp(self):
        app = Flask(__name__)
        Bootstrap(app)
        nav = Nav(app)
        app.secret_key = 'DUMMY'

        @app.route('/')
        def index():
            if current_user.is_authenticated:
                return 'OK'
            else:
                return redirect(url_for('commons.login'))

        @nav.navigation()
        def mynavbar():
            """Menu da aplicação."""
            items = [View('Home', 'index')]
            return Navbar('teste', *items)

        app.testing = True
        self.app = app.test_client()
        self.db = MongoClient(host=MONGODB_URI).unit_test
        login.login_manager.init_app(app)
        login.configure(app)
        login.DBUser.dbsession = self.db
        login.DBUser.add('ajna', 'ajna')

    def tearDown(self):
        self.db.drop_collection('users')
        rv = self.logout()
        assert rv is not None

    def login(self, username, senha):
        url = '/login'
        return self.app.post(url, data=dict(
            username=username,
            senha=senha,
        ), follow_redirects=True)

    def logout(self):
        return self.app.get('/logout', follow_redirects=True)

    def test_login_invalido(self):
        rv = self.login('none', 'error')
        print(rv)
        assert rv is not None
        assert b'401' in rv.data
        assert b'Unauthorized' in rv.data

    def test_login(self):
        rv = self.login('ajna', 'ajna')
        assert rv is not None
        assert b'OK' in rv.data

    def test_DBuser(self):
        auser = login.DBUser.get('ajna')
        assert auser.name == 'ajna'
        auser2 = login.DBUser.get('ajna', 'ajna')
        assert auser2.name == 'ajna'
        # Testa mundança de senha
        login.DBUser.add('ajna', '1234')
        auser3 = login.DBUser.get('ajna', 'ajna')
        assert auser3 is None
        auser4 = login.DBUser.get('ajna', '1234')
        assert auser4.name == 'ajna'

    def test_404(self):
        rv = self.app.get('/non_ecsiste')
        assert rv is not None
        assert b'404' in rv.data
