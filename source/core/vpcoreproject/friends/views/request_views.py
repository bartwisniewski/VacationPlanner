from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import TemplateView
from django.core.exceptions import ObjectDoesNotExist

from friends.models import Friends, UserToFriends, JoinRequest


class CreateJoinRequestView(TemplateView):
    success_url = reverse_lazy('friends-list')
    template_name = "friends/request_confirm.html"

    def get(self, request, *args, **kwargs):
        friends_id = self.kwargs['pk']
        try:
            friends = Friends.objects.get(id=friends_id)
            context = self.get_context_data(**kwargs)
            context['friends'] = friends
            return self.render_to_response(context)
        except ObjectDoesNotExist:
            messages.warning(self.request, f'Friends group with id {friends_id} does not exist')
        return HttpResponseRedirect(self.success_url)

    def post(self, request, *args, **kwargs):
        friends_id = self.kwargs['pk']
        # przejrzec wszystkie try'e
        try:
            friends = Friends.objects.get(id=friends_id)
        except ObjectDoesNotExist:
            messages.warning(self.request, f'Friends group with id {friends_id } does not exist')
        else:
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