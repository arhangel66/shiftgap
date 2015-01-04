from django.forms import ModelForm, TextInput

from .models import Shift


class ShiftForm(ModelForm):

    class Meta:
        model = Shift
        fields = ('start_time', 'end_time')
        widgets = {
            'datetime': TextInput(attrs={'blah': 'datetimepicker'})
        }