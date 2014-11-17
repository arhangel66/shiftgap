from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin

from django.views.generic import TemplateView
from django.http import HttpResponseRedirect

urlpatterns = patterns('',

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', TemplateView.as_view(template_name='welcome.html'), name='welcome'),

    # include your apps urls files below

    # Misc non django
    url(r'^404\.html$', TemplateView.as_view(template_name='404.html'), name='404'),
    url(r'^robots\.txt$', TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),
    url(r'^humans\.txt$', TemplateView.as_view(template_name='humans.txt', content_type='text/plain')),
    url(r'^crossdomain\.xml$', TemplateView.as_view(template_name='crossdomain.xml', content_type='text/xml')),
    url(r'^favicon.ico/$', lambda x: HttpResponseRedirect(settings.STATIC_URL+'favicon.ico')), #google chrome favicon fix
)
