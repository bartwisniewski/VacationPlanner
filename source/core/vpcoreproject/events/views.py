from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from events.models import Event, UserToEvent
from friends.models import Friends
# Create your views here.


class MyEventsListView(LoginRequiredMixin, ListView):

    model = Event
    paginate_by = 10

    def get_queryset(self):
        return Event.user_events(self.request.user).order_by('-id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        my_events = Event.user_events(self.request.user)
        my_friends_events = Event.user_friends_events(self.request.user)
        context['friends_events'] = my_friends_events.difference(my_events).order_by('-id')
        return context


class MissingEventsListView(LoginRequiredMixin, ListView):

    model = Event
    paginate_by = 10

    def get_queryset(self):
        my_friends_events = Event.objects.filter(friends__usertofriends__user=self.request.user)
        my_events = Event.user_events(self.request.user)
        missing_events = my_friends_events.difference(my_events)
        return missing_events.order_by('-id')


class EventCreateView(LoginRequiredMixin, CreateView):
    model = Event
    fields = ['name', 'friends', ]
    success_url = reverse_lazy('events-list')

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        form.fields['friends'].queryset = Friends.objects.filter(usertofriends__user=self.request.user)
        return form

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        self.object = form.save()
        UserToEvent(user=self.request.user, event=self.object, admin=True, owner=True).save()
        return HttpResponseRedirect(self.get_success_url())


class EventDetailView(DetailView):
    template_suffix_from_status = ["_detail", "_detail_1", "_detail_2"]
    model = Event

    def get_template_from_status(self):
        if 0 <= self.object.status <= len(EventDetailView.template_suffix_from_status):
            self.template_name_suffix = self.template_suffix_from_status[self.object.status]

    def get_context_0(self, context):
        context['date_proposals'] = ['test_date']
        # get  date proposals

    def get_context_status(self, context):
        context_status = [self.get_context_0]
        if 0 <= self.object.status <= len(context_status):
            context_status[self.object.status](context)

    def get_context_data(self, **kwargs):

        self.get_template_from_status()
        context = super().get_context_data(**kwargs)
        self.get_context_status(context)
        context['status_display'] = self.object.get_status_display()
        #
        return context


# class EventSingleObjectAdminView(LoginRequiredMixin, UserPassesTestMixin):
#     success_url = reverse_lazy('events-list')
#     permission_role = 'admin'
#     permission_denied_message = f'you are not {permission_role} of this event'
#
#     def test_func(self):
#         self.object = self.get_object()
#         return self.object.test_user_role(self.request.user, self.permission_role)
#
#     def handle_no_permission(self):
#         messages.warning(self.request, self.permission_denied_message)
#         return HttpResponseRedirect(self.get_success_url())
#
#
# class FriendsUpdateView(EventSingleObjectAdminView, UpdateView):
#     model = Friends
#     fields = '__all__'
#     template_name_suffix = '_update_form'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         related_users = self.object.usertofriends_set.all()
#         context['users'] = related_users
#         formset = self.object.get_users_formset()
#         context['users_formset'] = formset
#         return context
#
#     @owner_only
#     def update_members(self, request, *args, **kwargs):
#         count = int(request.POST.get('form-TOTAL_FORMS', 0))
#         post_data = request.POST
#         UserToFriendsUpdateManager.update_members(count, post_data)
#
#     def post(self, request, *args, **kwargs):
#         self.update_members(request, *args, **kwargs)
#         return super().post(request, *args, **kwargs)
#
#
# class FriendsDeleteView(FriendsSingleObjectView,  DeleteView):
#     model = Friends
#     permission_role = 'owner'
#     permission_denied_message = f'you are not {permission_role} of this group of friends'
