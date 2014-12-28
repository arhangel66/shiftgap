from django.db import models
from django.utils.translation import ugettext_lazy as _


class Shift(models.Model):
    start_time = models.DateTimeField(verbose_name=_('Start Time'))
    end_time = models.DateTimeField(verbose_name=_('End Time'))
    employee = models.CharField(max_length=64)