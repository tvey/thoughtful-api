from django.core.management.utils import get_random_secret_key
import dj_database_url

from .base import *

DEBUG = False

# env variables are set on the app directly with heroku config:set

SECRET_KEY = os.environ.get('SECRET_KEY', default=get_random_secret_key())

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS').split()

DATABASE_URL = os.environ.get('DATABASE_URL')

DATABASES = {
    'default': dj_database_url.config(
        default=DATABASE_URL, conn_max_age=500, ssl_require=True
    ),
}

MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')

STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'

STATIC_ROOT = BASE_DIR / 'staticfiles'
