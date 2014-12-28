from django.shortcuts import render
from django.views.generic import ListView
from .models import Shift


class ShiftListing(ListView):
    queryset = Shift.objects.all()