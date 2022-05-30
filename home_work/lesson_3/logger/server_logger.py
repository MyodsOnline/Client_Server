import os
import sys
import logging
from logging.handlers import TimedRotatingFileHandler

PATH = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.join(PATH, 'server.log')

log = logging.getLogger('app.server')

_formatter_file = logging.Formatter('%(asctime)s  %(levelname)-8s  %(module)-10s  %(message)s')
_formatter_stream = logging.Formatter('%(asctime)s  %(levelname)-8s  %(message)s')

file_handler = TimedRotatingFileHandler(PATH, when='D', interval=1, encoding='utf-8')
file_handler.setFormatter(_formatter_file)

stream_handler = logging.StreamHandler(sys.stderr)
stream_handler.setFormatter(_formatter_stream)
stream_handler.setLevel(logging.WARNING)

log.addHandler(file_handler)
log.addHandler(stream_handler)
log.setLevel(logging.DEBUG)

if __name__ == '__main__':
    log.critical('Критическая ошибка')
    log.error('Ошибка')
    log.debug('Отладочное сообщение')
    log.info('Информационное сообщение')
