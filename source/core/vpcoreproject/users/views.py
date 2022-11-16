from django.contrib.auth import login, get_user_model
from django.shortcuts import render
from django.views.generic.edit import FormView
from django.views.generic.base import TemplateView, View
from django.forms import ModelForm
from users.forms import MyUserCreationForm, FamilySizeForm

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


class RegisterFormView(View):
    template_name = 'users/register.html'
    user_form_class = MyUserCreationForm
    family_form_class = FamilySizeForm
    success_url = '/'

    def get(self, request, *args, **kwargs):
        user_form = self.user_form_class()
        #family_form = None
        # if request.GET.get('family'):
        family_form = self.family_form_class()
        forms = {'user_form': user_form, 'family_form': family_form}
        return render(request, self.template_name, forms)

    def post(self, request, *args, **kwargs):
        user_data = get_modelform_data_from_post(post=request.POST, form=self.user_form_class)
        family_data = get_modelform_data_from_post(post=request.POST, form=self.family_form_class)
        user_form = self.user_form_class(user_data)
        family_form = None
        #if family_data:
        #    family_form = self.family_form_class(request.POST)
        #    if family_form.is_valid():


        forms = {'user_form': user_form, 'family_form': family_form}
        return render(request, self.template_name, forms)

        # if form.is_valid():
        #     user = form.save()
        #     login(request, user)
        #     return self.form_valid(form)
        # else:
        #     return self.form_invalid(form)
