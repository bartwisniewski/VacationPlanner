from django import forms
from django.forms import ModelForm
from django.contrib.auth import login, get_user_model
from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.utils.translation import gettext_lazy as _
from users.models import FamilySize, MyUser


class MyUserUpdateForm(ModelForm):
    template_name = "users/form_snippet.html"

    class Meta:
        model = MyUser
        fields = ["username", "email"]


class MyUserCreationForm(UserCreationForm):
    template_name = "users/form_snippet.html"
    email = forms.EmailField(
        label=_("Email"),
        max_length=254,
        widget=forms.EmailInput(attrs={"autocomplete": "email"}),
    )

    class Meta:
        model = get_user_model()
        fields = ("username", "email")
        field_classes = {"username": UsernameField, "email": forms.EmailField}


class FamilySizeForm(ModelForm):
    template_name = "users/form_snippet.html"

    class Meta:
        model = FamilySize
        fields = "__all__"
