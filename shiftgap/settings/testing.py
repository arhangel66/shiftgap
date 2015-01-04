# -*- coding: utf8 -*-
from .base import *
__author__ = 'Derbichev Mikhail, arhangel662@gmail.com'

WSGI_APPLICATION = 'shiftgap.wsgi.application'

DATABASES = {
    "default": dict(
        ENGINE = "django.db.backends.sqlite3",
        NAME = ":memory:",
    )
}

INSTALLED_APPS += (
    'django_nose',
)



