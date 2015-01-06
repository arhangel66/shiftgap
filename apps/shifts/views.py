import datetime
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.views.generic.list import MultipleObjectMixin
import pytz

import simplejson as json
from django.shortcuts import render, redirect, render_to_response
from django.views.generic import ListView, CreateView
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.core.exceptions import ValidationError
from django.db import IntegrityError


from .models import Shift, UserAccount
from .forms import ShiftForm


def get_first_last_day_of_month(tz=pytz.utc):
    """
    Возвращает первую дату в месяце
    """
    days = int(datetime.datetime.now(tz=tz).strftime("%d"))-1
    date = datetime.date.today() - datetime.timedelta(days=days)
    return date


def get_list_days_of_week(dat=datetime.datetime.now(tz=pytz.utc)):
    """
    Возвращает первую дату в месяце
    """
    list_of_dates = []
    for i in range(-dat.weekday(), -dat.weekday()+7):
        d = dat + datetime.timedelta(days=i)
        list_of_dates.append(d)
    return list_of_dates



class ShiftListing(ListView):
    def get_queryset(self):
        return Shift.objects.all()

    def get_users(self, objects=None):
        """
        :return [user_id1, user_id2], {'user_id': UserObject}
        """
        user_list = []
        user_dict = {}
        if objects:
            user_list = list(set(objects.values_list('employee', flat=True)))
            for user in UserAccount.objects.filter(id__in=list(user_list)):
                user_dict[user.id] = user

        return [''] + user_list, user_dict

    def get_context_data(self, **kwargs):
        """
        Get the context for this view.
        """
        objects = kwargs.pop('object_list', self.object_list)
        objects_dict = {}
        for shift in objects:
            day = shift.start_time.strftime("%Y-%m-%d")
            user = shift.employee_id
            key = "%s_%s" % (user, day)
            objects_dict.setdefault(key, []).append(shift)

        strings_list, strings_dict = self.get_users(objects)
        rows_list, rows_dict = self.get_dates()
        table = []
        for i, string in enumerate(strings_list):
            line = []
            for j, row in enumerate(rows_list):
                cell = []
                if i == 0:
                    cell = rows_dict.get(row)
                elif j == 0:
                    cell = strings_dict.get(string)
                else:
                    key = "%s_%s" % (string, row)
                    cell = objects_dict.get(key)
                line.append(cell)
            table.append(line)
        context = {'table': table, 'request': self.request}
        return super(MultipleObjectMixin, self).get_context_data(**context)


    # def post(self, request, *args, **kwargs):
    #     try:
    #         import datetime
    #
    #         s = Shift.objects.create(
    #             # employee=self.request.POST['employee_name'],
    #             start_time=datetime.datetime(2014, 12, 30, 17, 0, 0, 0, tzinfo=pytz.timezone('UTC')),
    #             end_time=datetime.datetime(2014, 12, 30, 23, 0, 0, 0, tzinfo=pytz.timezone('UTC'))
    #         )
    #         return redirect(s.get_absolute_url())
    #     except ValidationError or IntegrityError as e:
    #         messages.warning(request, 'Invalid input ' + e.__str__())
    #         return redirect(reverse('shifts:shift_list'))

    def get_dates(self):
        dates = get_list_days_of_week()
        date_list = [None]
        date_dict = {}
        key = "%Y-%m-%d"
        show = "%a, %b %d, %Y"
        for dat in dates:
            date_key = dat.strftime(key)
            date_list.append(date_key)
            date_dict[date_key] = dat.strftime(show)
        return date_list, date_dict


class ShiftCreate(CreateView):
    form_class = ShiftForm
    model = Shift

    def form_valid(self, form):
        form.save()
        message = json.dumps({"status": True, "message": 'Success'})
        return HttpResponse("%s" % message)

    def form_invalid(self, form):
        message = json.dumps({"status": False, "message": form.errors.as_ul()})
        return HttpResponse("%s" % message)


def set_timezone(request):
    """
    Set timezone to the organization
    :param request:
    :return:
    """
    if request.method == 'POST':
        request.session['django_timezone'] = request.POST['timezone']
        print(request.session['django_timezone'])
        print(type(request.session['django_timezone']))
        return redirect('/')
    else:
        return render(request, 'shifts/set_timezone.html', {'timezones': pytz.common_timezones})


