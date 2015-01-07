from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

from .views import ShiftListing, ShiftCreate, ShiftUpdate, ShiftDelete

urlpatterns = patterns('',
                       url(r'^create/$', login_required(ShiftCreate.as_view()), name='shift_create'),
                       url(r'^$', login_required(ShiftListing.as_view()), name='shift_list'),
                       url(r'^update/(?P<pk>\d+)/$', login_required(ShiftUpdate.as_view()), name='shift_update'),
                       url(r'^delete/(?P<pk>\d+)/$', login_required(ShiftDelete.as_view()), name='shift_delete'),
                       # url(r'set-timezone/$', 'apps.shifts.views.set_timezone', name='set_timezone'),
                       )