from chat.views import ChatMixin
from django.contrib.auth import get_user_model, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic.base import TemplateView, View
from events.models import Event
from friends.models import Friends
from users.forms import FamilySizeForm, MyUserCreationForm, MyUserUpdateForm
from users.helpers import get_modelform_data_from_post

User = get_user_model()


class DashboardView(TemplateView, ChatMixin):
    template_name = "users/dashboard.html"

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if request.user.is_authenticated:
            context["joined"] = request.user.date_joined.strftime("%m/%d/%Y")
            self.add_chat_context(context, self.request)
            context["events"] = (
                Event.filter_by_user(self.request.user)
                .filter(status__lt=4)
                .order_by("-id")
            )
            context["friends"] = Friends.filter_by_user(self.request.user).order_by(
                "-id"
            )
        return self.render_to_response(context)


class UserRegisterEdit(View):
    template_name = "users/register.html"
    user_form_class = MyUserCreationForm
    family_form_class = FamilySizeForm
    success_url = "/"

    @staticmethod
    def get_user(request):
        if request.user.is_authenticated:
            return request.user
        return None

    @staticmethod
    def get_family(user):
        if user:
            return user.get_default_family()
        return None

    def get_post_data(self, post):
        user_data = get_modelform_data_from_post(post=post, form=self.user_form_class)
        family_data = get_modelform_data_from_post(
            post=post, form=self.family_form_class
        )
        return user_data, family_data

    def init_forms(self, request, user_post, family_post):
        user = self.get_user(request=request)
        user_form = self.user_form_class(user_post, instance=user)
        family = self.get_family(user)
        family_form = self.family_form_class(family_post, instance=family)
        family_active = 1 if family or family_post else 0
        return user_form, family_form, family_active

    def get(self, request, *args, **kwargs):
        print(request.user)
        user_form, family_form, family_active = self.init_forms(
            request=request, user_post=None, family_post=None
        )
        data = {
            "user_form": user_form,
            "family_form": family_form,
            "display_family": family_active,
        }
        return render(request, self.template_name, data)

    def post(self, request, *args, **kwargs):
        user_post, family_post = self.get_post_data(post=request.POST)
        user_form, family_form, family_active = self.init_forms(
            request=request, user_post=user_post, family_post=family_post
        )
        if (family_form.is_valid() or not family_active) and user_form.is_valid():
            user = user_form.save(commit=False)
            if family_active:
                family = family_form.save()
                user.default_family = family
            user.save()
            login(request, user)
            return HttpResponseRedirect(self.success_url)

        data = {
            "user_form": user_form,
            "family_form": family_form,
            "display_family": family_active,
        }
        return render(request, self.template_name, data)


class UserEditView(LoginRequiredMixin, UserRegisterEdit):
    template_name = "users/edit.html"
    user_form_class = MyUserUpdateForm
    family_form_class = FamilySizeForm
    success_url = "/user/edit"


class RegisterView(UserRegisterEdit):
    template_name = "users/register.html"
    user_form_class = MyUserCreationForm
    family_form_class = FamilySizeForm
    success_url = "/"
