from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin

from django.views.generic import TemplateView
from django.http import HttpResponseRedirect

urlpatterns = patterns('',
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^$', TemplateView.as_view(template_name='welcome.html'), name='welcome'),

                       # include your apps urls files below
                       url(r'shifts/', include('apps.shifts.urls', namespace='shifts'), name='shifts'),
                       url(r'personal/', include('apps.persons.urls', namespace='persons'), name='persons'),

                       # Misc non django
                       url(r'^404\.html$', TemplateView.as_view(template_name='404.html'), name='404'),
                       url(r'^jqueryui\.html$', TemplateView.as_view(template_name='jquery-ui.html'), name='jqueryui'),
                       url(r'^robots\.txt$', TemplateView.as_view(template_name='robots.txt',
                                                                  content_type='text/plain')),
                       url(r'^humans\.txt$', TemplateView.as_view(template_name='humans.txt',
                                                                  content_type='text/plain')),
                       url(r'^crossdomain\.xml$', TemplateView.as_view(template_name='crossdomain.xml',
                                                                       content_type='text/xml')),
                       # Google chrome favicon fix
                       url(r'^favicon.ico/$', lambda x: HttpResponseRedirect(settings.STATIC_URL+'favicon.ico')),
)