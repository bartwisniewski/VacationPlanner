from django import forms
from django.forms import ModelForm

from events.models import DateProposal, PlaceProposal


class DateInput(forms.DateInput):
    input_type = 'date'


class DateProposalForm(ModelForm):

    class Meta:
        model = DateProposal
        fields = ['start', 'end']
        widgets = {
            'start': DateInput(), 'end': DateInput()
        }


class PlaceProposalForm(ModelForm):

    class Meta:
        model = PlaceProposal
        exclude = ['user_event']
