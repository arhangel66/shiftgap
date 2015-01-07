# -*- coding: utf8 -*-
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.generic import CreateView, UpdateView
from apps.persons.forms import UserForm, MyUserChangeForm
from apps.shifts.models import UserAccount

__author__ = 'Derbichev Mikhail, arhangel662@gmail.com'


def personal_singin(request):
    """
    Singin
    """
    from django.contrib import auth
    if request.POST.get('login'):
        user = auth.authenticate(username=request.POST.get('login'), password=request.POST.get('password'))
        if user is not None:
            auth.login(request, user)
            next = request.GET.get('next')
            if next:
                return HttpResponseRedirect(next)
            else:
                return HttpResponseRedirect('/')
        else:
            error = 'login or password is incorrect'
    return render_to_response('auth.html', locals(), context_instance=RequestContext(request))


def personal_logout(request):
    # выход из системы
    logout(request)
    return HttpResponseRedirect("/")

class UserCreate(CreateView):
    form_class = UserForm
    model = UserAccount
    success_url = '/shifts/'  # reverse('shifts:shift_list')


class UserUpdate(UpdateView):
    form_class = MyUserChangeForm
    model = UserAccount
    success_url = '/shifts/'  # reverse('shifts:shift_list')
