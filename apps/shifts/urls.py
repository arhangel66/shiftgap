from django.conf.urls import patterns, url

from .views import ShiftListing

urlpatterns = patterns('',

                       url(r'^$', ShiftListing.as_view(), name='shift_listing'),
                       )