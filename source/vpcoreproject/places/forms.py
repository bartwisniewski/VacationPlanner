from django import forms
from django.forms import ModelForm

from places.models import Place, Owner, PlaceSize
from places.helpers import get_field_value_from_related_object
from users.forms import FamilySizeForm


class OwnerForm(ModelForm):
    class Meta:
        model = Owner
        fields = "__all__"
        labels = {"name": "Owner's name"}


class PlaceSizeForm(ModelForm):
    class Meta:
        model = PlaceSize
        fields = "__all__"


class PlaceForm(ModelForm):
    template_name = "places/form_snippet.html"
    sub_forms = [
        (OwnerForm, "owner"),
        (PlaceSizeForm, "size"),
        (FamilySizeForm, "capacity"),
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_subforms(kwargs.get("instance"))

    def add_subforms(self, instance=None):
        for sub_form in PlaceForm.sub_forms:
            added_fields = {}
            SubFormClass, prefix = sub_form
            for field in SubFormClass().fields.items():
                field_name, field_type = field
                form_field_name = prefix + "_" + field_name
                added_fields[form_field_name] = field_type
                self.initial[form_field_name] = get_field_value_from_related_object(
                    instance, prefix, field_name
                )
            self.fields.update(added_fields)

    def get_subform(self, sub_form):
        SubFormClass, prefix = sub_form
        data = {}
        for field in SubFormClass().fields.items():
            field_name, field_type = field
            field_name_in_form = prefix + "_" + field_name
            self.fields.pop(field_name_in_form)
            data[field_name] = self.data[field_name_in_form]
        return SubFormClass(data)

    def save_sub_forms(self):
        for sub_form in PlaceForm.sub_forms:
            SubFormClass, prefix = sub_form
            sub_form_instance = self.get_subform(sub_form)
            if sub_form_instance.is_valid():
                sub_object_instance = sub_form_instance.save()
                setattr(self.instance, prefix, sub_object_instance)

    def save(self, commit=True):
        if commit:
            self.save_sub_forms()
        return super().save(commit=commit)

    class Meta:
        model = Place
        exclude = ["owner", "capacity", "size", "created_by"]
