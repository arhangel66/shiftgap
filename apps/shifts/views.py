from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.edit import FormView, FormMixin
from django.views.generic.list import MultipleObjectMixin

from .models import Shift
from .forms import ShiftForm


class ShiftListing(FormMixin, ListView):
    queryset = Shift.objects.all()
    form_class = ShiftForm

    def get_context_data(self, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        kwargs = kwargs.copy()
        kwargs['form'] = form
        return kwargs