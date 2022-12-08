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

    model = Event

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        # context['book_list'] = Book.objects.all()
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
