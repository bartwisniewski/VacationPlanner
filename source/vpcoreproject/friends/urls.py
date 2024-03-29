from django.urls import path
from friends.views import friends_views, request_views

urlpatterns = [
    path("", friends_views.MyFriendsListView.as_view(), name="friends-list"),
    path("add", friends_views.FriendsCreateView.as_view(), name="friends-create"),
    path("<pk>/edit/", friends_views.FriendsUpdateView.as_view(), name="friends-edit"),
    path(
        "<pk>/delete/", friends_views.FriendsDeleteView.as_view(), name="friends-delete"
    ),
    path("<pk>/leave/", friends_views.FriendsLeaveView.as_view(), name="friends-leave"),
    path(
        "member/<pk>/delete/",
        friends_views.UserToFriendsDeleteView.as_view(),
        name="friends-member-delete",
    ),
    path("find/", request_views.FriendsFindView.as_view(), name="friends-find"),
    path(
        "<pk>/join/",
        request_views.CreateJoinRequestView.as_view(),
        name="create-join-request",
    ),
    path(
        "request/<pk>/answer",
        request_views.AnswerJoinRequestView.as_view(),
        name="answer-join-request",
    ),
]
