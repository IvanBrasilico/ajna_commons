"""Configuration of AJNA modules LOGs"""
import logging
import os
import sys

from flask_login import current_user


class MyFilter(object):
    """Log only especified level (not upper levels)"""

    def __init__(self, level):
        self.__level = level

    def filter(self, logRecord):
        return logRecord.levelno <= self.__level


class CustomAdapter(logging.LoggerAdapter):
    """
    This example adapter expects the passed in dict-like object to have a
    'connid' key, whose value in brackets is prepended to the log message.
    """

    def process(self, msg, kwargs):
        return '[%s][%s] %s' % (self.extra['username'],
                                self.extra['teste'], msg), kwargs


logging.basicConfig(level=os.environ.get('LOGLEVEL', 'INFO'))
logger = logging.getLogger('ajna')

fn = getattr(sys.modules['__main__'], '__file__')
root_path = os.path.abspath(os.path.dirname(fn))
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

if os.environ.get('DEBUG', 'None') == '1':
    logger.setLevel(logging.DEBUG)
    logger.addHandler(out_handler)
else:
    activity_handler.setLevel(logging.INFO)
    logger.addHandler(activity_handler)
    error_handler.setLevel(logging.WARNING)
    logger.addHandler(error_handler)
    out_handler.setLevel(logging.INFO)
    logger.addHandler(out_handler)
    logger.setLevel(logging.INFO)
    # Only show info, not warnings, erros, or critical in this log
    activity_handler.addFilter(MyFilter(logging.INFO))


def user_name(user):
    if user:
        return user.name
    return 'no user'


adapter = CustomAdapter(logger, {'username': user_name(
    current_user), 'teste': 'Nome de usuário'})

logger.info('Configuração de log efetuada')
