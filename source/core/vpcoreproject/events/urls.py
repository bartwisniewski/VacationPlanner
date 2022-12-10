from django.urls import path
from django.urls import include
from django.contrib.auth.urls import urlpatterns
from events import views
from events.views import event_list_views, event_detail_views, join_leave_views, event_manipulate_views, date_proposal_views

urlpatterns = [
    path('', event_list_views.MyEventsListView.as_view(), name="events-list"),
    path('add', event_manipulate_views.EventCreateView.as_view(), name="event-create"),
    path('<pk>/', event_detail_views.EventDetailView.as_view(), name="event-detail"),
    path('<pk>/edit/', event_manipulate_views.EventUpdateView.as_view(), name="event-edit"),
    path('member/<pk>/delete/', event_manipulate_views.UserToEventDeleteView.as_view(), name="event-member-delete"),
    path('<pk>/join/', join_leave_views.JoinView.as_view(), name="event-join"),
    path('<pk>/leave/', join_leave_views.LeaveView.as_view(), name="event-leave"),
    path('<pk>/date-propose/add/', date_proposal_views.DateProposalCreateView.as_view(), name="event-date-propose"),
    path('date-propose/<pk>/delete/', date_proposal_views.DateProposalDeleteView.as_view(), name="date-propose-delete"),
    path('date-propose/<pk>/vote/', date_proposal_views.DateProposalVoteView.as_view(), name="date-propose-vote"),
    path('date-propose/<pk>/unvote/', date_proposal_views.DateProposalUnvoteView.as_view(), name="date-propose-unvote"),
]
