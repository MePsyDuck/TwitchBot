import os

from dotenv import load_dotenv

load_dotenv()

DEBUG = os.getenv('DEBUG', 'False') == 'True'
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
CHANNELS = ['singsing' if not DEBUG else 'mepsyduck_']
PREFIX = '!!'
