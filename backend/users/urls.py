from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (ChangePasswordView, ForgotPasswordView, RegisterView, 
                    CustomTokenObtainPairView, UserAvatarUpdateView, UserProfileUpdateView, 
                    logout_view, verify_email, google_login)

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", CustomTokenObtainPairView.as_view(), name="login"),
    path("logout/", logout_view, name="logout"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    path("forgot-password/", ForgotPasswordView.as_view(), name="forgot-password"),
    path('profile/', UserProfileUpdateView.as_view(), name='user-profile-update'),
    path("profile/avatar/", UserAvatarUpdateView.as_view(), name="user-avatar-update"),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path("verify-email/<uuid:token>/", verify_email, name="verify-email"),
    path("google-login/", google_login, name="google-login"),
]
