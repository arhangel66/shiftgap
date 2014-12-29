from django.db import models
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError


class Shift(models.Model):
    start_time = models.DateTimeField(verbose_name=_('Start Time'))
    end_time = models.DateTimeField(verbose_name=_('End Time'))
    employee = models.CharField(max_length=64)

    def __str__(self):
        return self.employee + ' from ' + str(self.start_time) + ' to ' + str(self.end_time)

    def get_absolute_url(self):
        return reverse('shifts:shift_list')

    # def clean(self):
    #     if self.start_time >= self.end_time:
    #         raise ValidationError(_('Start time cannot be greater than or equal to end time.'))