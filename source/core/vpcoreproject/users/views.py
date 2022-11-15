from django.contrib.auth import login, get_user_model
from django.views.generic.edit import FormView
from django.views.generic.base import TemplateView
from .forms import MyUserCreationForm

# Create your views here.

User = get_user_model()


class DashboardView(TemplateView):
    template_name = "users/dashboard.html"

    def get(self, request, *args, **kwargs):

        context = self.get_context_data(**kwargs)
        if request.user.is_authenticated:
            context['joined'] = request.user.date_joined.strftime('%m/%d/%Y')

        return self.render_to_response(context)


class RegisterFormView(FormView):
    template_name = 'users/register.html'
    form_class = MyUserCreationForm
    success_url = '/'

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            user = form.save()
            login(request, user)
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
