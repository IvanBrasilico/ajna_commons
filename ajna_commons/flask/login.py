from urllib.parse import urljoin, urlparse

from flask import request
from flask_login import (LoginManager, UserMixin)
from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Length


login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.session_protection = 'strong'


class DBUser():
    dbsession = None

    def __init__(self, id):
        self.id = id
        self.name = str(id)

    @classmethod
    def get(cls, username, password=None):
        print('getting user', cls.dbsession)
        if cls.dbsession:
            if password:
                print({'username': username,
                       'password': password})
                user = cls.dbsession.users.find_one({'username': username,
                                                     'password': password})
            else:
                user = cls.dbsession.users.find_one({'username': username})
            print('User retrieved ', user)
            if user:
                return DBUser(username)
        else:
            if username:
                return DBUser(username)
        return None


# db.users.find({'username': 'ivan', 'password': 'ivan'})


class User(UserMixin):
    user_database = DBUser

    def __init__(self, id):
        self.id = id
        self.name = str(id)

    @classmethod
    def get(cls, username, password=None):
        dbuser = cls.user_database.get(username, password)
        if dbuser:
            print('Nome:', dbuser.name)
            return User(dbuser.name)
        return None


class LoginForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired(), Length(1, 50)])
    senha = PasswordField('Senha', validators=[DataRequired()])
    remember_me = BooleanField('Lembrar-me')
    submit = SubmitField('Entrar')


def authenticate(username, password):
    user_entry = User.get(username, password)
    print('User: ', user_entry)
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
