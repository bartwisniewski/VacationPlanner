from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import TemplateView
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView

from friends.models import Friends, UserToFriends, JoinRequest


class FriendsFindView(LoginRequiredMixin, ListView):
    template_name_suffix = '_find'
    model = Friends
    paginate_by = 10
    phrase_min_length = 3

    def get_queryset(self):
        phrase = self.request.GET.get('q', '')
        queryset = Friends.objects.exclude(usertofriends__user=self.request.user).order_by('-id')
        if len(phrase) >= self.phrase_min_length:
            queryset = queryset.filter(nickname__contains=phrase)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(ListView, self).get_context_data(**kwargs)
        phrase = self.request.GET.get('q', '')
        if len(phrase) >= self.phrase_min_length:
            context['phrase'] = phrase
        elif phrase:
            messages.warning(self.request, f'Search phrase too short min {self.phrase_min_length} characters')
        return context

    def post(self, request, *args, **kwargs):
        my_url = request.path
        print(my_url)
        q = self.request.POST.get('phrase', '')
        if q:
            my_url += f"?q={q}"
        return HttpResponseRedirect(my_url)


class CreateJoinRequestView(TemplateView):
    success_url = reverse_lazy('friends-list')
    template_name = "friends/request_confirm.html"

    def get(self, request, *args, **kwargs):
        friends_id = self.kwargs['pk']
        friends = Friends.get_or_warning(friends_id, request)
        if friends:
            context = self.get_context_data(**kwargs)
            context['friends'] = friends
            return self.render_to_response(context)
        return HttpResponseRedirect(self.success_url)

    def post(self, request, *args, **kwargs):
        friends_id = self.kwargs['pk']
        friends = Friends.get_or_warning(friends_id, request)
        if friends:
            user = request.user
            join_request, created = JoinRequest.objects.get_or_create(user=user, friends=friends)
            if created:
                messages.info(self.request, f'Join request created')
            else:
                messages.warning(self.request, f'You have already sent a request to join this group')
        return HttpResponseRedirect(self.success_url)


class AnswerJoinRequestView(TemplateView):
    success_url = reverse_lazy('friends-list')
    template_name = "friends/confirm.html"

    def get_object(self):
        request_id = self.kwargs['pk']
        try:
            return JoinRequest.objects.get(id=request_id)
        except ObjectDoesNotExist:
            messages.warning(self.request, f'Join request does not exist')
        return None

    def get(self, request, *args, **kwargs):
        join_request = self.get_object()
        if join_request:
            accept = self.request.GET.get('accept', False)

            context = self.get_context_data(**kwargs)
            context['object'] = join_request
            context['action'] = 'accept' if accept else 'reject'
            return self.render_to_response(context)

        return HttpResponseRedirect(self.success_url)

    def post(self, request, *args, **kwargs):
        join_request = self.get_object()
        if join_request:
            accept = self.request.GET.get('accept', False)
            if accept:
                UserToFriends(user=join_request.user, friends=join_request.friends).save()
                messages.info(self.request, f'Join request accepted')
            else:
                messages.info(self.request, f'Join request rejected')
            join_request.delete()

        return HttpResponseRedirect(self.success_url)
