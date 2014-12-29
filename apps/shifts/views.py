import pytz

from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView

from .models import Shift
from .forms import ShiftForm


class ShiftListing(ListView):
    queryset = Shift.objects.all()


class ShiftCreate(CreateView):
    form_class = ShiftForm
    model = Shift


def set_timezone(request):
    if request.method == 'POST':
        request.session['django_timezone'] = request.POST['timezone']
        return redirect('/')
    else:
        return render(request, 'shifts/set_timezone.html', {'timezones': pytz.common_timezones})