# -*- coding: utf8 -*-
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import ModelForm
from apps.shifts.models import UserAccount

__author__ = 'Derbichev Mikhail, arhangel662@gmail.com'


class UserForm(UserCreationForm):
    class Meta:
        model = UserAccount
        fields = ('username', 'email', 'first_name', 'last_name', 'organization', 'position', 'timezone')


class MyUserChangeForm(ModelForm):
    class Meta:
        model = UserAccount
        fields = ('username', 'email', 'first_name', 'last_name', 'organization', 'position', 'timezone')
