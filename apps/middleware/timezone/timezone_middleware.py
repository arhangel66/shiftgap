import pytz

from django.utils import timezone


class TimezoneMiddleware(object):

    def process_request(self, request):
        if request.user.id and hasattr(request.user, 'timezone'):
            timezone.activate(pytz.timezone(request.user.timezone))
        else:
            timezone.activate(pytz.timezone('UTC'))
