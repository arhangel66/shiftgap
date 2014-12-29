from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.generic import ListView, CreateView
from .models import Shift
from .forms import ShiftForm


class ShiftListing(ListView):
    queryset = Shift.objects.all()


class ShiftCreate(CreateView):
    form_class = ShiftForm
    model = Shift