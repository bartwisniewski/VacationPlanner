from django.urls import path
from django.urls import include
from django.contrib.auth.urls import urlpatterns
from events import views

urlpatterns = [
    path('', views.MyEventsListView.as_view(), name="events-list"),
    path('add', views.EventCreateView.as_view(), name="event-create"),
    path('<pk>/', views.EventDetailView.as_view(), name="event-detail"),
]