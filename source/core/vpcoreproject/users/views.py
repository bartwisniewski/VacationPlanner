from django.contrib.auth import login, get_user_model
from django.shortcuts import render
from django.views.generic.edit import FormView
from django.views.generic.base import TemplateView, View
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


class RegisterFormView(View):
    template_name = 'users/register.html'
    user_form_class = MyUserCreationForm
    add_form_class = FamilySizeForm
    success_url = '/'

    def get(self, request, *args, **kwargs):
        user_form = self.user_form_class()
        add_form = None
        if request.GET.get('family'):
            add_form = self.add_form_class()
        forms = {'user_form': user_form, 'add_form': add_form}
        return render(request, self.template_name, forms)

    def post(self, request, *args, **kwargs):
        print(request.POST)
        user_form = self.user_form_class()
        add_form = self.add_form_class()
        forms = {'user_form': user_form, 'add_form': add_form}
        return render(request, self.template_name, forms)
        # user_form = self.user_form_class(request.POST)
        # if form.is_valid():
        #     user = form.save()
        #     login(request, user)
        #     return self.form_valid(form)
        # else:
        #     return self.form_invalid(form)
