from django import forms
from django.forms import ModelForm

from events.models import DateProposal


class DateInput(forms.DateInput):
    input_type = 'date'


class DateProposalForm(ModelForm):

    class Meta:
        model = DateProposal
        fields = ['start', 'end']
        widgets = {
            'start': DateInput(), 'end': DateInput()
        }
