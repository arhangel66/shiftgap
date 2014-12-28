from .base import *

# THIS NEEDS TO BE UPDATED BEFORE USING IN REAL PRODUCTION

WSGI_APPLICATION = 'shiftgap.wsgi.application'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True if environ.get('DEBUG', 'false').lower() == 'true' else False

TEMPLATE_DEBUG = False


import dj_database_url
DATABASES = {
    'default': dj_database_url.config()
}
DATABASES['default']['ATOMIC_REQUESTS'] = True

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
ALLOWED_HOSTS = [x.strip() for x in environ.get('ALLOWED_HOSTS', '').split(',') if x]

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

# Output logs to heroku logplex
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
        }
    }
}

# redirect all requests to SSL
SECURE_SSL_REDIRECT = True