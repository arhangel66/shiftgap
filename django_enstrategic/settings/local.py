from .base import *

WSGI_APPLICATION = 'django_enstrategic.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'boiler',
    }
}

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['*']

# Static files

STATIC_ROOT = "../staticgenerated/"

INSTALLED_APPS += (
    'django.contrib.admindocs',
    'debug_toolbar',
)

DEBUG_TOOLBAR_PATCH_SETTINGS = True

# ADMIN_FOR = ('django.contrib.admindocs',)  # no longer needed in django1.7

MIDDLEWARE_CLASSES += (
    'django.contrib.admindocs.middleware.XViewMiddleware',  # for admindocs
)

# run celery tasks synchronously during development
CELERY_ALWAYS_EAGER = True

# We don't want to redirect to SSL in development
SECURE_SSL_REDIRECT = False

DEBUG_TOOLBAR_PANELS = [
    'debug_toolbar.panels.versions.VersionsPanel',
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.settings.SettingsPanel',
    'debug_toolbar.panels.headers.HeadersPanel',
    'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    'debug_toolbar.panels.staticfiles.StaticFilesPanel',
    'debug_toolbar.panels.templates.TemplatesPanel',
    'debug_toolbar.panels.cache.CachePanel',
    'debug_toolbar.panels.signals.SignalsPanel',
    'debug_toolbar.panels.logging.LoggingPanel',
    'debug_toolbar.panels.redirects.RedirectsPanel',
]