from django.contrib.auth import login, get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.generic.edit import FormView
from django.views.generic.base import TemplateView, View
from django.forms import ModelForm
from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.core.exceptions import ObjectDoesNotExist

from users.forms import MyUserCreationForm, MyUserUpdateForm, FamilySizeForm

# Create your views here.

User = get_user_model()


class DashboardView(TemplateView):
    template_name = "users/dashboard.html"

    def get(self, request, *args, **kwargs):

        context = self.get_context_data(**kwargs)
        if request.user.is_authenticated:
            context['joined'] = request.user.date_joined.strftime('%m/%d/%Y')

        return self.render_to_response(context)


def get_modelform_data_from_post(post: dict, form: type(ModelForm)) -> dict:
    return_dict = {}
    temp_form_instance = form()
    for field in temp_form_instance.fields:
        if field in post.keys():
            return_dict[field] = post.get(field, None)
    return return_dict


# class UserRegisterEditMixin:
#     self.user_form_class(instance = user)

class UserEditView(View):
    template_name = 'users/edit.html'
    user_form_class = MyUserUpdateForm
    family_form_class = FamilySizeForm
    success_url = '/'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        user = request.user
        user_form = self.user_form_class(instance=user)
        display_family = 1
        try:
            family = user.default_family
        except ObjectDoesNotExist:
            family = None
            display_family = 0
        family_form = self.family_form_class(instance=family)
        data = {'user_form': user_form, 'family_form': family_form, 'display_family': display_family}
        return render(request, self.template_name, data)

    def post(self, request, *args, **kwargs):
        print(request.POST)


class RegisterView(View):
    template_name = 'users/register.html'
    user_form_class = MyUserCreationForm
    family_form_class = FamilySizeForm
    success_url = '/'

    def get(self, request, *args, **kwargs):
        user_form = self.user_form_class()
        family_form = self.family_form_class()
        data = {'user_form': user_form, 'family_form': family_form, 'display_family': 0}
        return render(request, self.template_name, data)

    def split_data(self, post: dict):
        user_data = get_modelform_data_from_post(post=post, form=self.user_form_class)
        family_data = get_modelform_data_from_post(post=post, form=self.family_form_class)
        return user_data, family_data

    def check_family(self, family_data: dict):
        family_active = 1 if family_data else 0
        if family_data:
            family_form = self.family_form_class(family_data)
        else:
            family_form = self.family_form_class()
        return family_form, family_active

    def post(self, request, *args, **kwargs):
        user_data, family_data = self.split_data(post=request.POST)
        user_form = self.user_form_class(user_data)
        family_form, family_active = self.check_family(family_data=family_data)

        if (family_form.is_valid() or not family_active) and user_form.is_valid():
            user = user_form.save(commit=False)
            if family_active:
                family = family_form.save()
                user.default_family = family
            user.save()
            login(request, user)
            return HttpResponseRedirect(self.success_url)
        else:
            data = {'user_form': user_form, 'family_form': family_form, 'display_family': family_active}
            return render(request, self.template_name, data)
