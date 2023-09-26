from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.decorators.clickjacking import xframe_options_sameorigin
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, FormView, UpdateView
from django.views.generic.list import ListView
from events.models import Event, PlaceProposal, UserToEvent
from places.forms import PlaceForm, PlaceScrapForm
from places.models import Place, PlaceScrap
from places.scrapper import logic as scrapper_logic
from rest_framework.response import Response
from rest_framework.views import APIView


class MyPlacesListView(LoginRequiredMixin, ListView):
    model = Place
    paginate_by = 10

    def get_queryset(self):
        return Place.user_places(self.request.user).order_by("-id")


class PlaceDetailView(LoginRequiredMixin, DetailView):
    model = Place

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["type_display"] = self.object.get_type_display()
        context["region_display"] = self.object.get_region_display()
        return context


class PlaceFrameView(LoginRequiredMixin, DetailView):
    template_name = "places/place_object.html"
    model = Place

    @xframe_options_sameorigin
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class PlaceCreateView(LoginRequiredMixin, CreateView):
    model = Place
    form_class = PlaceForm
    success_url = reverse_lazy("places-list")

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        form.instance.created_by = self.request.user
        return super().form_valid(form)

    def get_event(self):
        event_id = self.request.GET.get("event")
        if event_id:
            return Event.get_or_warning(event_id, self.request)
        return None

    def create_place_proposal(self):
        event = self.get_event()
        if not event:
            return
        place = self.object
        user = self.request.user
        user_event = UserToEvent.get_or_warning(user, event, self.request)
        if user_event and place:
            PlaceProposal(place=place, user_event=user_event).save()

    def get_success_url(self):
        event_id = self.request.GET.get("event")
        if event_id:
            return reverse("event-detail", kwargs={"pk": event_id})
        return PlaceCreateView.success_url

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            response = self.form_valid(form)
            self.create_place_proposal()
            return response
        else:
            return self.form_invalid(form)


class PlaceDeleteView(UserPassesTestMixin, DeleteView):
    model = Place
    success_url = reverse_lazy("places-list")
    permission_role = "admin"
    permission_denied_message = "you are not owner of this place"

    def test_func(self):
        place = self.get_object()
        return place.created_by == self.request.user

    def handle_no_permission(self):
        messages.warning(self.request, self.permission_denied_message)
        return HttpResponseRedirect(self.get_success_url())


class PlaceUpdateView(UserPassesTestMixin, UpdateView):
    model = Place
    form_class = PlaceForm
    template_name_suffix = "_form"
    success_url = reverse_lazy("places-list")
    permission_denied_message = "you have not created this place"

    def test_func(self):
        self.object = self.get_object()
        return self.object.created_by == self.request.user

    def handle_no_permission(self):
        messages.warning(self.request, self.permission_denied_message)
        return HttpResponseRedirect(self.get_success_url())

    def get_form(self, form_class=None):
        """Return an instance of the form to be used in this view."""
        if form_class is None:
            form_class = self.get_form_class()
        form_kwargs = self.get_form_kwargs()
        return form_class(**form_kwargs)


class PlaceScrapView(LoginRequiredMixin, FormView):
    template_name = "places/place_scrap.html"
    form_class = PlaceScrapForm
    success_url = reverse_lazy("place-scrap-list")

    def form_valid(self, form):
        task_id = scrapper_logic.new_scrap(form)
        if task_id:
            self.success_url = reverse_lazy(
                "place-scrap-result", kwargs={"task_id": task_id}
            )
            PlaceScrap(task_id=task_id, created_by=self.request.user).save()
        else:
            messages.warning(self.request, "scrapping could not be started")
        return super().form_valid(form)


class PlaceScrapGetData(APIView):
    def get(self, request, task_id, format=None):
        print("rest api working")
        scrapper_result = scrapper_logic.get_result(task_id)
        return Response(data=scrapper_result, status=200)


class PlaceScrapResultView(UserPassesTestMixin, TemplateView):
    model = PlaceScrap
    template_name = "places/place_scrap_result.html"
    reject_url = reverse_lazy("place-srap-list")
    permission_denied_message = "you have not ordered this scrap"

    def get_object(self):
        task_id = self.kwargs.get("task_id", None)
        return PlaceScrap.get_or_warning(task_id=task_id, request=self.request)

    def test_func(self):
        self.object = self.get_object()
        if self.object:
            return self.object.created_by == self.request.user
        return False

    def handle_no_permission(self):
        messages.warning(self.request, self.permission_denied_message)
        return HttpResponseRedirect(PlaceScrapResultView.reject_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        task_id = self.object.task_id
        if task_id:
            context["task_id"] = task_id
            context["endpoint"] = reverse_lazy(
                "place-scrap-api", kwargs={"task_id": task_id}
            )
            result = scrapper_logic.get_result(task_id)
            context.update(result)
        return context


class MyPlaceScrapListView(LoginRequiredMixin, ListView):
    model = PlaceScrap
    paginate_by = 10

    def get_queryset(self):
        return PlaceScrap.user_scraps(self.request.user).order_by("-id")
