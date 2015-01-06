from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

from .views import ShiftListing, ShiftCreate

urlpatterns = patterns('',
                       url(r'^create/$', ShiftCreate.as_view(), name='shift_create'),
                       url(r'^$', login_required(ShiftListing.as_view()), name='shift_list'),
                       url(r'set-timezone/$', 'apps.shifts.views.set_timezone', name='set_timezone'),
                       )