from django.urls import path
from places import views

urlpatterns = [
    path('', views.MyPlacesListView.as_view(), name="places-list"),
    path('add/', views.PlaceCreateView.as_view(), name="place-create"),
]
