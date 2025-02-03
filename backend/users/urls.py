from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import ForgotPasswordView, RegisterView, CustomTokenObtainPairView, logout_view

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", CustomTokenObtainPairView.as_view(), name="login"),
    path("logout/", logout_view, name="logout"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("forgot_password/", ForgotPasswordView.as_view(), name="forgot_password"),
]
