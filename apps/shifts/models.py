from django.contrib.auth.models import User, UserManager, AbstractBaseUser
from django.db import models
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.template.loader import get_template
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError


class Organization(models.Model):
    name = models.CharField(max_length=100, verbose_name="Name of organization")
    timezone = models.CharField(max_length=100, verbose_name="Timezone of organization", default="America/Chicago")

    def __str__(self):
        return u"%s" % self.name

    def get_list_of_users(self):
        users = UserAccount.objects.filter(organization=self.id)
        return users

from pytz import common_timezones
tz_choces = []
for tz in common_timezones:
    tz_choces.append((tz, tz))


class UserAccount(User):
    organization = models.ForeignKey(Organization, blank=True, null=True, verbose_name="Organization")
    position = models.CharField(max_length=100, blank=True, null=True, default="Salesperson")
    timezone = models.CharField(max_length=100, verbose_name="Timezone", default="Europe/London", choices=tz_choces)

    objects = UserManager()

    def __str__(self):
        return u"%s %s %s" % (self.organization, self.last_name, self.first_name)

    def get_names(self):
        return "%s %s" % (self.first_name, self.last_name)

    def show(self):
        return """<div class="" style=''>
        <div class="brown">%s %s</div>
        <div style="color:#000; font-weight:normal;">%s</div>
        </div>
        """ % (self.first_name, self.last_name, self.organization.name if self.organization else '')

    def _is_this_shift_of_my_org(self, shift):
        if shift.employee_id == self.id:
            return True

        if shift.employee.organization_id and shift.employee.organization_id == self.organization_id:
            return True
        return False

    def can_update_shift(self, shift):
        if self._is_this_shift_of_my_org(shift) or self.is_superuser:
            return True
        return False

    def can_create_shift(self):
        return True

    def can_delete_shift(self, shift):
        if self._is_this_shift_of_my_org(shift) or self.is_superuser:
            return True
        return False

    def can_create_this_shift(self, shift):
        if self._is_this_shift_of_my_org(shift) or self.is_superuser:
            return True
        return False

    def get_users_for_create(self):
        org = self.organization
        if self.is_superuser:
            users = UserAccount.objects.all()
        else:
            if org:
                users = UserAccount.objects.filter(Q(id=self.id) | Q(organization_id=org.id))
            else:
                users = UserAccount.objects.filter(Q(id=self.id))
        return users



class Shift(models.Model):
    start_time = models.DateTimeField(verbose_name=_('Start Time'))
    end_time = models.DateTimeField(verbose_name=_('End Time'))
    employee = models.ForeignKey(UserAccount, verbose_name="UserAccount")

    def __init__(self, *args, **kwargs):
        self.template = ''
        super(Shift, self).__init__(*args, **kwargs)

    def __str__(self):
        return self.employee.first_name + ' from ' + str(self.start_time) + ' to ' + str(self.end_time)

    def get_absolute_url(self):
        return reverse('shifts:shift_list')

    def show(self):
        from django.template import Template, Context
        t = get_template('shifts/blocks/shift_week.html')
        t = get_template('shifts/blocks/shift_month.html')
        return t.render(Context({'shift': self}))
