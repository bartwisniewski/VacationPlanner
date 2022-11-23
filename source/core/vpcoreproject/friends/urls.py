from django.urls import path
from django.urls import include
from django.contrib.auth.urls import urlpatterns
from friends import views

urlpatterns = [
    path('', views.MyFriendsListView.as_view(), name="friends-list"),
    path('add', views.FriendsCreateView.as_view(), name="friends-create"),
    path('<pk>/edit/', views.FriendsUpdateView.as_view(), name="friends-edit"),
    path('<pk>/delete/', views.FriendsDeleteView.as_view(), name="friends-delete"),
    path('member/<pk>/delete/', views.UserToFriendsDeleteView.as_view(), name="member-delete"),
    path('find', views.FriendsListView.as_view(), name="friends-find"),
    path('<pk>/join/', views.CreateJoinRequestView.as_view(), name="create-join-request"),
    path('request/<pk>/answer', views.AnswerJoinRequestView.as_view(), name="answer-join-request"),
]