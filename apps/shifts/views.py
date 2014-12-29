from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.generic import ListView, CreateView
from django.utils import timezone


from .models import Shift
from .forms import ShiftForm


class ShiftListing(ListView):
    queryset = Shift.objects.all()

    def get(self, request, *args, **kwargs):
        timezone.activate('Canada/Mountain')
        return super(ListView, self).get(request, *args, **kwargs)


class ShiftCreate(CreateView):
    form_class = ShiftForm
    model = Shift