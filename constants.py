import logging
import os


BB_HOST = 'https://ibank.asb.by'
MTB_HOST = 'https://new.mybank.by'

# Session lifetime in seconds.
SESSION_LIFETIME = int(os.environ.get('SESSION_LIFETIME', 3600))

STAGE = os.environ.get('STAGE')

PASSWORDS_TABLE = f'passwords-{STAGE}'


if STAGE:
    # We are under lambda - log everything into stdout.
    logging.basicConfig(level=logging.DEBUG)