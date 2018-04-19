"""Configuration of AJNA modules LOGs.

Aqui são configurados os diversos arquivos e métodos de logs que serão
comuns aos módulos do sistema AJNA.

Todo módulo deve importar este arquivo e usar o objeto logger criado
para gravar eventos importantes.

"""
import logging
import os
import sys

from flask_login import current_user
from raven.handlers.logging import SentryHandler

from ajna_commons.flask.conf import SENTRY_DSN


class MyFilter(object):
    """Log only especified level (not upper levels)."""

    def __init__(self, level):
        """Configura level desejado."""
        self.__level = level

    def filter(self, logRecord):
        """Retorna true se filtro no nível configurado."""
        return logRecord.levelno <= self.__level


class CustomAdapter(logging.LoggerAdapter):
    """Formata string de log.

    This example adapter expects the passed in dict-like object to have a
    'connid' key, whose value in brackets is prepended to the log message.
    """

    def process(self, msg, kwargs):
        """Returna string formatada."""
        return '[%s][%s] %s' % (self.extra['username'],
                                self.extra['teste'], msg), kwargs


logging.basicConfig(level=os.environ.get('LOGLEVEL', 'INFO'))
logger = logging.getLogger('ajna')

fn = getattr(sys.modules['__main__'], '__file__')
root_path = os.path.abspath(os.path.dirname(fn))
if root_path.find('.exe') != -1:
    root_path = os.path.dirname(__file__)
log_file = os.path.join(root_path, 'error.log')
print('Fazendo log de erros e alertas no arquivo ', log_file)
error_handler = logging.FileHandler(log_file)

activity_file = os.path.join(root_path, 'access.log')
print('Fazendo log de atividade no arquivo ', activity_file)
activity_handler = logging.FileHandler(activity_file)

out_handler = logging.StreamHandler(sys.stdout)


formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
error_handler.setFormatter(formatter)
activity_handler.setFormatter(formatter)
out_handler.setFormatter(formatter)
error_handler.setLevel(logging.WARNING)

if os.environ.get('DEBUG', 'None') == '1':
    logger.setLevel(logging.DEBUG)
    logger.addHandler(out_handler)
    logger.addHandler(error_handler)
else:
    activity_handler.setLevel(logging.INFO)
    logger.addHandler(activity_handler)
    logger.addHandler(error_handler)
    out_handler.setLevel(logging.INFO)
    logger.addHandler(out_handler)
    sentry_handler = None
    if SENTRY_DSN:
        sentry_handler = SentryHandler(SENTRY_DSN)
        sentry_handler.setFormatter(formatter)
        sentry_handler.setLevel(logging.WARNING)
        sentry_handler.setFormatter(formatter)
        logger.addHandler(sentry_handler)
    logger.setLevel(logging.INFO)
    # Only show info, not warnings, erros, or critical in this log
    activity_handler.addFilter(MyFilter(logging.INFO))


def user_name(user):
    """Recupera nome do usuário ativo. Se não houver retorna 'no user'."""
    if user:
        return user.name
    return 'no user'


adapter = CustomAdapter(logger, {'username': user_name(
    current_user), 'teste': 'Nome de usuário'})

logger.info('Configuração de log efetuada')
