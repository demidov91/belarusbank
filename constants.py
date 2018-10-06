import logging
import os

BASE_DIR = os.path.dirname(__file__)
BASE_PATH = os.environ.get('BASE_PATH', '/')

BB_HOST = 'https://ibank.asb.by'
MTB_HOST = 'https://new.mybank.by'

# Session lifetime in seconds. 15 days.
SESSION_LIFETIME = int(os.environ.get('SESSION_LIFETIME', 3600 * 24 * 15))

STAGE = os.environ.get('STAGE')

PASSWORDS_TABLE = f'passwords-{STAGE}'


if STAGE:
    # We are under serverless/lambda - log everything into LambdaLoggingHandler.
    logging.getLogger().setLevel(logging.DEBUG)
