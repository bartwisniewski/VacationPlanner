from django.http import HttpResponseRedirect
from django.urls import reverse
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import View, TemplateView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, DeleteView

from places.forms import PlaceForm
from places.models import Place


class MyPlacesListView(LoginRequiredMixin, ListView):

    model = Place
    paginate_by = 10

    def get_queryset(self):
        return Place.user_places(self.request.user).order_by('-id')


class PlaceCreateView(LoginRequiredMixin, CreateView):
    model = Place
    form_class = PlaceForm
