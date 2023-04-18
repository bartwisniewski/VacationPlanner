from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import TemplateView
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic.list import ListView

from friends.models import Friends, UserToFriends, JoinRequest


class FriendsFindView(LoginRequiredMixin, ListView):
    template_name_suffix = "_find"
    model = Friends
    paginate_by = 10
    phrase_min_length = 3

    def get_queryset(self):
        phrase = self.request.GET.get("q", "")
        queryset = Friends.objects.exclude(
            usertofriends__user=self.request.user
        ).order_by("-id")
        if len(phrase) >= self.phrase_min_length:
            queryset = queryset.filter(nickname__contains=phrase)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(ListView, self).get_context_data(**kwargs)
        phrase = self.request.GET.get("q", "")
        if len(phrase) >= self.phrase_min_length:
            context["phrase"] = phrase
        elif phrase:
            messages.warning(
                self.request,
                f"Search phrase too short min {self.phrase_min_length} characters",
            )
        return context

    def post(self, request, *args, **kwargs):
        my_url = request.path
        q = self.request.POST.get("phrase", "")
        if q:
            my_url += f"?q={q}"
        return HttpResponseRedirect(my_url)


class CreateJoinRequestView(LoginRequiredMixin, TemplateView):
    success_url = reverse_lazy("friends-list")
    template_name = "friends/request_confirm.html"

    def get(self, request, *args, **kwargs):
        friends_id = self.kwargs["pk"]
        friends = Friends.get_or_warning(friends_id, request)
        if friends:
            context = self.get_context_data(**kwargs)
            context["friends"] = friends
            return self.render_to_response(context)
        return HttpResponseRedirect(self.success_url)

    def post(self, request, *args, **kwargs):
        friends_id = self.kwargs["pk"]
        friends = Friends.get_or_warning(friends_id, request)
        if friends:
            user = request.user
            join_request, created = JoinRequest.objects.get_or_create(
                user=user, friends=friends
            )
            if created:
                messages.info(self.request, "Join request created")
            else:
                messages.warning(
                    self.request, "You have already sent a request to join this group"
                )
        return HttpResponseRedirect(self.success_url)


class AnswerJoinRequestView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    success_url = reverse_lazy("friends-list")
    template_name = "friends/confirm.html"
    model = UserToFriends
    permission_denied_message = "you are not permited to answer this request"

    def test_func(self):
        self.object = self.get_object()
        if not self.object:
            return False

        return self.object.friends.test_user_role(self.request.user, "admin")

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return super().handle_no_permission()
        messages.warning(self.request, self.permission_denied_message)
        return HttpResponseRedirect(self.success_url)

    def get_object(self):
        request_id = self.kwargs["pk"]
        try:
            return JoinRequest.objects.get(id=request_id)
        except ObjectDoesNotExist:
            messages.warning(self.request, "Join request does not exist")
        return None

    def get(self, request, *args, **kwargs):
        join_request = self.get_object()
        if join_request:
            accept = self.request.GET.get("accept", False)

            context = self.get_context_data(**kwargs)
            context["object"] = join_request
            context["action"] = "accept" if accept else "reject"
            return self.render_to_response(context)

        return HttpResponseRedirect(self.success_url)

    def post(self, request, *args, **kwargs):
        join_request = self.get_object()
        if join_request:
            accept = self.request.GET.get("accept", False)
            if accept == "True":
                UserToFriends(
                    user=join_request.user, friends=join_request.friends
                ).save()
                messages.info(self.request, "Join request accepted")
            else:
                messages.info(self.request, "Join request rejected")
            join_request.delete()

        return HttpResponseRedirect(self.success_url)
