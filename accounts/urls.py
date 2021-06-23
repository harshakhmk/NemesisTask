from django.urls import reverse, path, include
from .views import (
    RegisterView,
    LoginView,
    Logout,
    home,
    account_details,
)  # AccountDetailsView
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path("", home, name="index"),
    path("home/", home, name="home"),
    path("register/", RegisterView, name="register"),
    path("login/", LoginView, name="login"),
    path("logout/", Logout, name="logout"),
    path("account-details/", account_details, name="account-details"),
]
