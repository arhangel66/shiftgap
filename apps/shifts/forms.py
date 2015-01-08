import datetime
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, AbstractUser
from django.db.models import Q
from django.forms import ModelForm, TextInput, CharField, Select, ModelChoiceField, DateField, Form, ChoiceField

from .models import Shift, UserAccount, Organization


class ShiftForm(ModelForm):
    employee = ModelChoiceField(required=True, queryset=UserAccount.objects.all(),
                                widget=Select(attrs={'class': 'form-control'}))
    class Meta:
        model = Shift
        fields = ('start_time', 'end_time', 'employee')
        widgets = {
            'start_time': TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'end_time': TextInput(attrs={'class': 'form-control ', 'readonly': 'readonly'}),
            'employee': Select(attrs={'class': 'form-control '})
        }

    def __init__(self, *args, **kwargs):
        super(ShiftForm, self).__init__(*args, **kwargs)
        if 'initial' in kwargs and 'user' in kwargs['initial']:
            user = kwargs['initial']['user']
            self.fields["employee"].queryset = user.get_users_for_create()
            self.initial["employee"] = kwargs['initial']['user'].id


    def clean(self):
        super(ShiftForm, self).clean()
        # self._errors["employee"] = self.error_class([u'You can choose only yourself or employee of your company'])
        return self.cleaned_data


class ShiftListForm(Form):
    TYPES = (
       ('user-date', "week"),
       ('week-day_of_week', "month"),
       ('week-user', "custom"),
    )

    start_date = DateField(widget=TextInput(attrs={'class': 'form-control', 'placeholder': 'From date'}))
    end_date = DateField(widget=TextInput(attrs={'class': 'form-control', 'placeholder': 'End date'}))
    employee = ModelChoiceField(queryset=UserAccount.objects.all(), widget=Select(attrs={'class': 'form-control', }))
    organization = ModelChoiceField(queryset=Organization.objects.all(), widget=Select(attrs={'class': 'form-control'}))
    type_view = ChoiceField(choices=TYPES, widget=Select(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        super(ShiftListForm, self).__init__(*args, **kwargs)
        if 'initial' in kwargs and 'user' in kwargs['initial']:
            user = kwargs['initial']['user']
            self.fields["employee"].queryset = user.get_users_for_create()
            self.initial["employee"] = kwargs['initial']['user'].id

