import os
from .settings import *  # noqa
from .settings import BASE_DIR

SECRET_KEY = os.environ["SECRET_KEY"]
ALLOWED_HOSTS = [os.environ["WEBSITE_HOSTNAME"]]
CSRF_TRUSTED_ORIGINS = [os.environ["WEBSITE_HOSTNAME"]]
DEBUG = False

INSTALLED_APPS = [
    'shop',
    'users',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("NAME"),
        "USER": os.environ.get("USER"),
        "PASSWORD": os.environ.get("PASSWORD"),
        "HOST": os.environ.get("HOST"),
        "PORT": os.environ.get("DB_PORT")
    }
}
