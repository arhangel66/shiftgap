"""
Django settings for ensretail project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

from os.path import join, abspath, dirname
from os import environ

here = lambda *dirs: join(abspath(dirname(__file__)), *dirs)

BASE_DIR = here('..', '..')  # two directories up

root = lambda *dirs: join(abspath(BASE_DIR), *dirs)  # project directory

from django.utils.crypto import get_random_string
SECRET_KEY = environ.get("SECRET_KEY", get_random_string(50, "abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)"))

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Application definition
DJANGO_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.formtools',
)

THIRD_PARTY_APPS = (
    'djangosecure',
)

YOUR_APPS = (
    'apps.shifts',
    'apps.persons',
)

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + YOUR_APPS

MIDDLEWARE_CLASSES = (

    'djangosecure.middleware.SecurityMiddleware',  # django-secure package
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'apps.middleware.users.users_middleware.UsersMiddleware',
    'apps.middleware.timezone.timezone_middleware.TimezoneMiddleware',
)

ROOT_URLCONF = 'shiftgap.urls'

# Internationalization

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LOCALE_PATHS = (
    root('translations'),
)

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    root('static'),
)

# Template files
TEMPLATE_DIRS = (
    root('templates'),
)

# Administrators
EMAIL_BACKEND = 'django.core.mail.backends.dummy.EmailBackend'

ADMINS = (('Mike', 'mike@eth0.ca'), ('Mike', 'michael.mackinnon@enstrategic.com'))
SERVER_EMAIL = 'mike@eth0.ca'

# So messages will work with bootstrap we need error to make danger
from django.contrib.messages import constants as message_constants
MESSAGE_TAGS = {message_constants.DEBUG: 'debug',
                message_constants.INFO: 'info',
                message_constants.SUCCESS: 'success',
                message_constants.WARNING: 'warning',
                message_constants.ERROR: 'danger', }



# Redis on Heroku
#REDIS_URL = environ.get('REDISTOGO_URL', 'redis://localhost')

# Using celery on Heroku must limit connections on free/starter plan
# JSON only is most secure
## BROKER_URL = REDIS_URL
#BROKER_TRANSPORT = 'redis'
#CELERY_TASK_SERIALIZER = 'json'
#CELERY_ACCEPT_CONTENT = ['json']
#CELERY_RESULT_BACKEND = REDIS_URL + '/1'
#CELERY_REDIS_MAX_CONNECTIONS = 2

AWS_STORAGE_BUCKET_NAME = environ.get('AWS_STORAGE_BUCKET_NAME')
AWS_ACCESS_KEY_ID = environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = environ.get('AWS_SECRET_ACCESS_KEY')
AWS_CALLING_FORMAT = environ.get('AWS_CALLING_FORMAT')

LOGIN_URL = '/personal/login/'
LOGIN_REDIRECT_URL = '/personal/'
AUTH_PROFILE_MODULE = 'apps.shifts.UserAccount'
CUSTOM_USER_MODEL = 'apps.shifts.UserAccount'