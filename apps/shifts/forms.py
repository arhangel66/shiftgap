from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, AbstractUser
from django.forms import ModelForm, TextInput, CharField, Select, ModelChoiceField

from .models import Shift, UserAccount


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





