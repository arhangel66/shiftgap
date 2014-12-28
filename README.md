enstrategic boilerplate
========================

* Django 1.7
* HTML5 boilerplate
* Bootstrap
* Jquery
* Modernizr


If you rename top level directory django_enstrategic change the following:

> django_enstrategic/settings/base.py
>   ROOT_URLCONF = 'django_enstrategic.urls'


To create a custom settings file...create a new file in the settings subdirectory

> from .base import *

Then define your custom settings. Set environment variable DJANGO_SETTINGS_MODULE to your new settings file


Templates
=========
* __ (two underscores) - template is meant to be extended
* _ (one underscore) - template is meant to be included (not used on its own)
* (no underscores) - template is meant for end use


Improving site security
=======================

Ideally, you should not store your site's ``SECRET_KEY`` setting in version control. Instead, it should be read
from the Heroku config as follows:

::

    from django.utils.crypto import get_random_string
    SECRET_KEY = os.environ.get("SECRET_KEY", get_random_string(50, "abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)"))

You can then generate a secret key in your Heroku config with the following command:

::

    $ heroku config:set SECRET_KEY=`openssl rand -base64 32`

It's also recommended that you configure Python to generate a new random seed every time it boots.

::

    $ heroku config:set PYTHONHASHSEED=random