import os

HOST = 'https://ibank.asb.by'

USERNAME = ''
PASSWORD = ''
EXTREMELY_SIMPLE_KEY = '123'
DEBUG = False

BASE_DIR = os.path.dirname(__file__)

import logging
logging.basicConfig(filename='/home/demidov/belarusbank/log.log', level=logging.DEBUG)


try:
    from local_settings import *
except ImportError:
    pass
