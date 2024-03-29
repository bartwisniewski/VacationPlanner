from django import forms


class UserEventsRoleForm(forms.Form):
    template_name = "events/role_form_snippet.html"
    id = forms.IntegerField(required=False)
    username = forms.CharField(required=False)
    admin = forms.BooleanField(required=False)
    owner = forms.BooleanField(required=False)
