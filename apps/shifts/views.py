from copy import copy
import datetime
import re
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.utils.decorators import method_decorator
from django.views.generic.list import MultipleObjectMixin
import pytz

import simplejson as json
from django.shortcuts import render, redirect, render_to_response
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.core.exceptions import ValidationError
from django.db import IntegrityError


from .models import Shift, UserAccount
from .forms import ShiftForm, ShiftListForm


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


def get_list_days_beetween_dates(start_date, end_date):
    dat = start_date
    list_of_dates = []
    while end_date >= dat:
        list_of_dates.append(dat)
        dat += datetime.timedelta(days=1)

    return list_of_dates


class ShiftListing(ListView):
    def get_queryset(self):
        shifts = Shift.objects.filter(employee_id__gte=0)
        if not hasattr(self, 'request') or not self.request.method == "POST":
            start_date = datetime.datetime(2015, 1, 5)
            period = 8
            end_date = start_date + datetime.timedelta(days=period)
            self.request.session['post'] = {
                'start_date': start_date,
                'end_date': end_date,
                'type_view': 'week-day_of_week',
            }
        data = self.request.session['post']

        if data.get('start_date'):
            shifts = shifts.filter(start_time__gte=data['start_date'])

        if data.get('end_date'):
            shifts = shifts.filter(start_time__lte=data['end_date'])

        if data.get('employee'):
            shifts = shifts.filter(employee_id=data.get('employee'))

        if data.get('organization'):
            shifts = shifts.filter(employee__organization=data.get('organization'))

        if hasattr(self, 'request'):
            if not self.request.user.is_superuser:
                user_id = self.request.user
                organization_id = self.request.user.organization_id
                shifts = shifts.filter(Q(employee_id=user_id) | Q(employee__organization=organization_id))
        return shifts

    def post(self, request, *args, **kwargs):
        if request.POST['start_date']:
            self.request.session['post'] = {
                'start_date': datetime.datetime.strptime("%s 00:00:00" % request.POST['start_date'][:10], "%Y-%m-%d %H:%M:%S"),
                'end_date': datetime.datetime.strptime("%s 23:59:59" % request.POST['end_date'][:10], "%Y-%m-%d %H:%M:%S"),
                'employee': request.POST['employee'],
                'organization': request.POST['organization'],
                'type_view': request.POST['type_view']
            }
        return self.get(request, *args, **kwargs)

    def get_users(self, objects=None):
        """
        :return [user_id1, user_id2], {'user_id': UserObject}
        """
        user_list = []
        user_dict = {}
        if objects:
            user_list = list(set(objects.values_list('employee', flat=True)))
            for user in UserAccount.objects.filter(id__in=list(user_list)):
                user_dict[user.id] = user.show()

        return user_list, user_dict

    def get_context_data(self, **kwargs):
        """
        Get the context for this view.
        """
        datas = self.request.session.pop('post')
        types = ['user', 'date', 'week', 'day_of_week']
        string, row = datas['type_view'].split('-')
        # string = types[3]
        # row = types[0]

        objects = kwargs.pop('object_list', self.object_list)
        objects_dict = {}
        for shift in objects:
            params = {
                'date': shift.start_time.strftime("%Y-%m-%d"),
                'user': shift.employee_id,
                'week': int(shift.start_time.strftime('%U')),
                'day_of_week': int(shift.start_time.strftime('%w')),
            }

            key = "%s_%s" % (params.get(string), params.get(row))
            objects_dict.setdefault(key, []).append(shift)

        params = {
            'user': self.get_users(objects),
            'date': self.get_dates(datas.get('start_date'), datas.get('end_date')),
            'week': self.get_weeks(),
            'day_of_week': self.get_days_of_week()
        }

        calendar_list, calendar_dict = self.get_dates(datas.get('start_date')+datetime.timedelta(days=-30), datas.get('end_date')+datetime.timedelta(days=30), key="%U_%w", show='%d')

        strings_list, strings_dict = params.get(string)
        rows_list, rows_dict = params.get(row)
        strings_list = [''] + strings_list
        rows_list = [''] + rows_list
        table = []
        for i, string in enumerate(strings_list):
            line = []
            for j, row in enumerate(rows_list):
                cell = {'content': [], 'title': ''}
                if i == 0:
                    cell['content'] = rows_dict.get(row)
                elif j == 0:
                    cell['content'] = strings_dict.get(string)
                else:
                    key = "%s_%s" % (string, row)
                    cell['content'] = objects_dict.get(key)
                    if datas['type_view'] == 'week-day_of_week':
                        cell['title'] = calendar_dict.get(key)
                line.append(cell)
            table.append(line)

        datas['start_date'] = datas['start_date'].strftime("%Y-%m-%d")
        datas['end_date'] = datas['end_date'].strftime("%Y-%m-%d")
        list_form = ShiftListForm(datas)
        # else:
        #     list_form = ShiftListForm(self.request.POST)

        context = {'table': table, 'request': self.request, 'list_form': list_form}
        return super(MultipleObjectMixin, self).get_context_data(**context)

    def get_dates(self, start_date=None, end_date=None, key="%Y-%m-%d", show="%a, %b %d, %Y"):
        dates = get_list_days_of_week()
        if start_date and end_date:
            dates = get_list_days_beetween_dates(start_date, end_date)
        date_list = []
        date_dict = {}
        for dat in dates:
            date_key = dat.strftime(key)
            if key == "%U_%w":
                date_key = "%s_%s" % (int(dat.strftime('%U')), int(dat.strftime('%w')))
            date_list.append(date_key)
            date_dict[date_key] = dat.strftime(show)
        return date_list, date_dict

    def get_weeks(self, start_date=None, end_date=None):
        if not start_date:
            weeks = range(int(datetime.datetime.now().strftime('%U')), int(datetime.datetime.now().strftime('%U'))+4)
        week_list = []
        week_dict = {}
        for week in weeks:
            week_key = week
            week_list.append(week_key)
            week_dict[week_key] = "Week #%s" % week
        return week_list, week_dict

    def get_days_of_week(self):
        date_list = list(range(0, 7))
        date_dict = {
            1: 'Monday',
            2: 'Tuesday',
            3: 'Wednesday',
            4: 'Thursday',
            5: 'Friday',
            6: 'Saturday',
            0: 'Sunday'
        }
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

    def get_initial(self):
        return {'user': self.request.user}


class ShiftUpdate(UpdateView):
    form_class = ShiftForm
    model = Shift

    def form_valid(self, form):
        form.save()
        message = json.dumps({"status": True, "message": 'Success'})
        return HttpResponse("%s" % message)

    def form_invalid(self, form):
        message = json.dumps({"status": False, "message": form.errors.as_ul()})
        return HttpResponse("%s" % message)

    def dispatch(self, request, *args, **kwargs):
        shifts = Shift.objects.filter(id=kwargs['pk'])
        if shifts:
            shift = shifts[0]
            if not self.request.user.can_update_shift(shift):
                return HttpResponse("You can't Update this shift")
        return super(ShiftUpdate, self).dispatch(request, *args, **kwargs)


class ShiftDelete(DeleteView):
    model = Shift
    success_url = '/shifts/'

    def dispatch(self, request, *args, **kwargs):
        shifts = Shift.objects.filter(id=kwargs['pk'])
        if shifts:
            shift = shifts[0]
            if not self.request.user.can_delete_shift(shift):
                return HttpResponse("You can't Delete this shift")
        return super(ShiftDelete, self).dispatch(request, *args, **kwargs)

