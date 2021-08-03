import os

import dotenv

from .base import *

dotenv.load_dotenv(BASE_DIR / '.env')

DEBUG = True

SECRET_KEY = os.environ.get('SECRET_KEY')

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS').split()
