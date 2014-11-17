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