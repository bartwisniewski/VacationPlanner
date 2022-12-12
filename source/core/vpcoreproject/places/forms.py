from django import forms
from django.forms import ModelForm

from places.models import Place, Owner, PlaceSize
from users.forms import FamilySizeForm


class OwnerForm(ModelForm):

    class Meta:
        model = Owner
        fields = '__all__'
        labels = {
            "name": "Owner's name"
        }


class PlaceSizeForm(ModelForm):

    class Meta:
        model = PlaceSize
        fields = '__all__'


class PlaceForm(ModelForm):
    template_name = "places/form_snippet.html"
    sub_forms = [(OwnerForm, 'owner'), (PlaceSizeForm, 'size'), (FamilySizeForm, 'family')]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_subforms()

    def add_subforms(self):
        for sub_form in PlaceForm.sub_forms:
            added_fields = {}
            SubFormClass, prefix = sub_form
            for field in SubFormClass().fields.items():
                added_fields[prefix+'_'+field[0]] = field[1]
            self.fields.update(added_fields)

    class Meta:
        model = Place
        exclude = ['owner', 'capacity', 'size', 'created_by']
