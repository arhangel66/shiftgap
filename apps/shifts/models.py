from django.contrib.auth.models import User
from django.db import models
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError


class Organization(models.Model):
    name = models.CharField(max_length=100, verbose_name="Name of organization")
    timezone = models.CharField(max_length=100, verbose_name="Timezone of organization", default="America/Chicago")

    def __unicode__(self):
        return u"%s" % self.name

    def get_list_of_users(self):
        return []


class UserAccount(User):
    organization = models.ForeignKey(Organization, blank=True, null=True, verbose_name="Organization")
    position = models.CharField(max_length=100, blank=True, null=True)
    timezone = models.CharField(max_length=100, verbose_name="Timezone", default="America/Chicago")

    def __unicode__(self):
        return u"%s %s" % (self.organization, self.first_name)

    def can_update_shift(self, shift):
        return True

    def can_create_shift(self):
        return True

    def can_delete_shift(self, shift):
        return True

    def can_create_this_shift(self, shift):
        return True


class Shift(models.Model):
    start_time = models.DateTimeField(verbose_name=_('Start Time'))
    end_time = models.DateTimeField(verbose_name=_('End Time'))
    employee = models.ForeignKey(UserAccount, verbose_name="UserAccount")

    def __str__(self):
        return self.employee + ' from ' + str(self.start_time) + ' to ' + str(self.end_time)

    def get_absolute_url(self):
        return reverse('shifts:shift_list')

    # def clean(self):
    #     if self.start_time >= self.end_time:
    #         raise ValidationError(_('Start time cannot be greater than or equal to end time.'))