from django.urls import path
from places import views

urlpatterns = [
    path('add', views.PlaceCreateView.as_view(), name="place-create"),
]
