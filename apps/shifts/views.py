import pytz

from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.core.exceptions import ValidationError
from django.db import IntegrityError


from .models import Shift
from .forms import ShiftForm


class ShiftListing(ListView):
    queryset = Shift.objects.all()

    def post(self, request, *args, **kwargs):
        try:
            import datetime

            s = Shift.objects.create(
                # employee=self.request.POST['employee_name'],
                start_time=datetime.datetime(2014, 12, 30, 17, 0, 0, 0, tzinfo=pytz.timezone('UTC')),
                end_time=datetime.datetime(2014, 12, 30, 23, 0, 0, 0, tzinfo=pytz.timezone('UTC'))
            )
            return redirect(s.get_absolute_url())
        except ValidationError or IntegrityError as e:
            messages.warning(request, 'Invalid input ' + e.__str__())
            return redirect(reverse('shifts:shift_list'))


class ShiftCreate(CreateView):
    form_class = ShiftForm
    model = Shift


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