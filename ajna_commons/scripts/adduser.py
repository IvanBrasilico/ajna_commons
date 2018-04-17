"""Um script simples para adicionar um usuário ao BD.

Uso:
   python ajna_commons/scripts/adduser.py -u=username -p=password

"""
import click
from pymongo import MongoClient
from ajna_commons.flask.login import DBUser
from ajna_commons.flask.conf import (BSON_REDIS, DATABASE, MONGODB_URI,
                                     PADMA_URL, SECRET, redisdb)


@click.command()
@click.option('-u', help='Nome de usuário', prompt='Digite o nome de usuário')
@click.option('-p', help='Senha', prompt='Agora digite a senha')
def adduser(u, p):
    """Insere usuário no Banco de Dados."""
    DBUser.dbsession = MongoClient(host=MONGODB_URI)[DATABASE]
    return DBUser.add(u, p)


if __name__ == '__main__':
    print(adduser())
