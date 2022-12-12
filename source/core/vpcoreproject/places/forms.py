from django import forms
from django.forms import ModelForm

from places.models import Place


class PlaceForm(ModelForm):

    owner = forms.ImageField()

    class Meta:
        model = Place
        fields = ['start', 'end']
        widgets = {
            'start': DateInput(), 'end': DateInput()
        }


class PlaceProposalForm(ModelForm):

    class Meta:
        model = PlaceProposal
        exclude = ['user_event']
