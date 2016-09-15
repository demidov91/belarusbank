import os

BB_HOST = 'https://ibank.asb.by'
MTB_HOST = 'https://new.mybank.by'

BB_USERNAME = ''
BB_PASSWORD = ''

MTB_USERNAME = ''
MTB_PASSWORD = ''

EXTREMELY_SIMPLE_KEY = '123'
DEBUG = False

BASE_DIR = os.path.dirname(__file__)

import logging
logging.basicConfig(filename=os.path.join(BASE_DIR, 'log.log'), level=logging.DEBUG)


try:
    from local_settings import *
except ImportError:
    pass
