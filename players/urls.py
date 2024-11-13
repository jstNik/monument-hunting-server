from django.urls import path

from .views import LoginView, SignupView

app_name = "players"

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("signup/", SignupView.as_view(), name="signup")
]