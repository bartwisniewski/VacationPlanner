from django.urls import include, path
from users import views

urlpatterns = [
    path("", include("django.contrib.auth.urls")),
    path("", views.DashboardView.as_view(), name="dashboard"),
    path("register", views.RegisterView.as_view(), name="register"),
    path("edit", views.UserEditView.as_view(), name="user-edit"),
]
