import os

DEBUG = os.getenv('DEBUG', 'False') == 'True'

ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
CHANNELS = ['singsing', 'mepsyduck_']
PREFIX = '!!'

COOLDOWN = 5 if not DEBUG else 0
DEV_NICK = 'mepsyduck_'
