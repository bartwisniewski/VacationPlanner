from django.urls import path
from places import views

urlpatterns = [
    path("", views.MyPlacesListView.as_view(), name="places-list"),
    path("<pk>/", views.PlaceDetailView.as_view(), name="place"),
    path("<pk>/frame", views.PlaceFrameView.as_view(), name="place-frame"),
    path("add", views.PlaceCreateView.as_view(), name="place-create"),
    path("<pk>/delete", views.PlaceDeleteView.as_view(), name="place-delete"),
    path("<pk>/edit", views.PlaceUpdateView.as_view(), name="place-edit"),
    path("scrap/new", views.PlaceScrapView.as_view(), name="place-scrap"),
    path(
        "scrap/<str:task_id>",
        views.PlaceScrapResultView.as_view(),
        name="place-scrap-result",
    ),
    path("scrap", views.MyPlaceScrapListView.as_view(), name="place-scrap-list"),
    path(
        "scrap/api/<str:task_id>/",
        views.PlaceScrapGetData.as_view(),
        name="place-scrap-api",
    ),
]
