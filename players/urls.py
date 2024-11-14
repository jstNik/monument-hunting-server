from django.urls import path

from .views import LoginView, SignupView, TokenRefreshView, TokenVerifyView

app_name = "players"

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("signup/", SignupView.as_view(), name="signup"),
    path("auth/refresh/", TokenRefreshView.as_view(), name="refresh"),
    path("auth/verify/", TokenVerifyView.as_view(), name="verify")
]
