# -*- coding: utf8 -*-
from apps.shifts.models import UserAccount
from django.contrib.auth.models import User
__author__ = 'Derbichev Mikhail, arhangel662@gmail.com'

import pytz

from django.utils import timezone


class UsersMiddleware(object):
    def process_request(self, request):
        if request.user.id and not hasattr(request.user, 'timezone'):
            user = UserAccount.objects.filter(id=request.user.id)
            if user:
                request.user = user[0]
