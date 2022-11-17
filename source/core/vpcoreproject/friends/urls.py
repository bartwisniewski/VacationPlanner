from django.urls import path
from django.urls import include
from django.contrib.auth.urls import urlpatterns
from friends import views

urlpatterns = [
    path('', views.MyFriendsListView.as_view(), name="friends-list"),
    path('add', views.FriendsCreateView.as_view(), name="friends-create")
]