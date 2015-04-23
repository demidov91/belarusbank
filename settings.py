HOST = 'https://ibank.asb.by'

USERNAME = ''
PASSWORD = ''
EXTREMELY_SIMPLE_KEY = '123'
DEBUG = False

try:
    from local_settings import *
except ImportError:
    pass
