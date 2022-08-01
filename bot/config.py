import os

DEBUG = os.getenv('DEBUG', 'False') == 'True'
COOLDOWN = 5 if not DEBUG else 0
DEV_NICK = 'mepsyduck_'

ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
WEBHOOK_SECRET = os.getenv('WEBHOOK_SECRET')
CALLBACK_URL = os.getenv('CALLBACK_URL')
LISTEN_PORT = os.getenv('LISTEN_PORT')

CHANNELS = ['singsing', 'mepsyduck_']
PREFIX = '!!'

DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'

