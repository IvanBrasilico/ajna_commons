"""Funções e views que dão suporte ao LOGIN das aplicações centralizadas.

Classes para acessar os usuários do Banco de Dados
Views padrão login e logout (Flask)
Funções e classes para gerenciar login e usuários (Flask Login)

Para utilizar, importar e chamar configure(app) em uma aplicação Flask

DBUser.dbsession deve receber a conexão com o BD.
"""
from urllib.parse import urljoin, urlparse
from flask import abort, redirect, render_template, request, url_for
from flask_login import (LoginManager, UserMixin)
from flask_login import login_required, login_user, logout_user
# from urllib.parse import urlparse, urljoin
from werkzeug.security import generate_password_hash, check_password_hash

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.session_protection = 'strong'

# Customized login error
#  http://flask.pocoo.org/docs/0.12/patterns/packages/
# https://flask-login.readthedocs.io/en/latest/ - Customizing the login
login_manager.login_message = u'Efetue login para começar.'


def configure(app):
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        """View para efetuar login."""
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('senha')
            registered_user = authenticate(username, password)
            if registered_user is not None:
                print('Logged in..')
                print(login_user(registered_user))
                # print('Current user ', current_user)
                next_url = request.args.get('next')
                if not is_safe_url(next_url):
                    return abort(400)
                return redirect(next_url or url_for('index'))
            else:
                return abort(401)
        else:
            return render_template('login.html', form=request.form)

    @app.route('/logout')
    @login_required
    def logout():
        """View para efetuar logout."""
        logout_user()
        next = request.args.get('next')
        if not is_safe_url(next):
            next = None
        return redirect(next or url_for('index'))


@login_manager.unauthorized_handler
def unauthorized():
    message = 'Não autorizado! ' + \
        'Efetue login novamente com usuário e senha válidos.'
    return redirect(url_for('login',
                            message=message))


class DBUser():
    dbsession = None

    def __init__(self, id, password=None):
        self.id = id
        self.name = str(id)
        self._password = password

    @classmethod
    def add(cls, username, password):
        """Cria usuário ou muda senha se ele existe."""
        if not cls.dbsession:
            raise Exception('Sem conexão com o Banco de Dados!')
        encripted = cls.encript(password)
        cursor = cls.dbsession.users.update(
            {'username': username},
            {'username': username,
             'password': encripted},
            upsert=True)
        print('cursor', cursor)
        return DBUser.get(username, password)

    @classmethod
    def encript(cls, password):
        """Receives plan text password, returns encripted version"""
        if password is None:
            return ''
        return generate_password_hash(password)

    def check(self, encripted):
        """Checks user password against encripted version"""
        if self._password is None:
            return False
        return check_password_hash(encripted, self._password)

    @classmethod
    def get(cls, username, password=None):
        """Test if user exists, and if passed, if password
        is correct
        returns DBUser or None
        """
        print('Getting user. dbsession=', cls.dbsession)
        if cls.dbsession:
            # print('DBSEssion ', cls.dbsession)
            dbuser = DBUser(username, password)
            user = cls.dbsession.users.find_one(
                {'username': username})
            if password:
                encripted = user['password']
                print('username', username,
                      'passed password', password)
                print('encripted', encripted)
                if not dbuser.check(encripted):
                    return None
            return DBUser(username)
        else:
            if username:
                if not password:
                    return DBUser(username, password)
                if username == password:
                    return DBUser(username, password)
        return None


class User(UserMixin):
    user_database = DBUser

    def __init__(self, id):
        self.id = id
        self.name = str(id)

    @classmethod
    def get(cls, username, password=None):
        dbuser = cls.user_database.get(username, password)
        if dbuser:
            return User(dbuser.name)
        return None


def authenticate(username, password):
    user_entry = User.get(username, password)
    # print('authenticate user entry ', user_entry)
    return user_entry


@login_manager.user_loader
def load_user(userid):
    user_entry = User.get(userid)
    return user_entry


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
        ref_url.netloc == test_url.netloc
