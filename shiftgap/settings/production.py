from .base import *

# THIS NEEDS TO BE UPDATED BEFORE USING IN REAL PRODUCTION

WSGI_APPLICATION = 'ensretail.deploywsgi.application'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

TEMPLATE_DEBUG = False

from os import environ

ENS_PRODUCTION = environ.get('ENS_PRODUCTION', None)

if ENS_PRODUCTION == 'True':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': environ.get('ENS_DB_NAME'),
            'USER': environ.get('ENS_DB_USER'),
            'PASSWORD': environ.get('ENS_DB_PASSWORD'),
            'HOST': environ.get('ENS_DB_HOST'),
            'PORT': environ.get('ENS_DB_PORT'),
            'CONN_MAX_AGE': 1800,
            'OPTIONS': {
                'sslmode': 'verify-full',
                'sslrootcert': 'ensretail/rds-ssl-ca-cert.pem'
            }
        },
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': environ.get('ENS_DB_NAME'),
            'USER': environ.get('ENS_DB_USER'),
            'PASSWORD': environ.get('ENS_DB_PASSWORD'),
            'HOST': environ.get('ENS_DB_HOST'),
            'PORT': environ.get('ENS_DB_PORT'),
        },
    }

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
ALLOWED_HOSTS = [
    '.herokuapp.com',
    # enter your custom domains here
]

# Static files from heroku help
import os

PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))
STATIC_ROOT = 'staticfiles'

INSTALLED_APPS += (

)

MIDDLEWARE_CLASSES += (

)


# If using Sentry error aggregation
# RAVEN_CONFIG = {
#     'dsn': environ.get('ENS_DSN', None),
# }

# This should be removed and the final domain explicitly allowed
# CORS_ORIGIN_ALLOW_ALL = True
#
# CORS_ALLOW_HEADERS = (
#     'x-requested-with',
#     'content-type',
#     'accept',
#     'origin',
#     'authorization',
#     'authorization-token',
#     'x-csrftoken'
# )