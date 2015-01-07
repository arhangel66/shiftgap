# -*- coding: utf8 -*-
from apps.persons.views import UserCreate, UserUpdate

__author__ = 'Derbichev Mikhail, arhangel662@gmail.com'
from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin

from django.views.generic import TemplateView
from django.http import HttpResponseRedirect

urlpatterns = patterns('apps.persons.views',
url(r'^login/$', 'personal_singin', name='singin'),
url(r'^logout/$', 'personal_logout', name='logout'),
url(r'user_create/$', UserCreate.as_view(), name='user_create'),
url(r'^set_timezone/(?P<pk>\d+)/edit/$', UserUpdate.as_view(), name='user_update'),
)