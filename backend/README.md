# XploreAI - Django

**Bước 1:** Cài đặt Django và Django REST Framework
Trước tiên, bạn cần cài đặt Django và DRF để tạo backend API.

```sh
pip install django djangorestframework djangorestframework-simplejwt mysqlclient django-cors-headers
```

**Bước 2:** Khởi tạo dự án Django
```sh
django-admin startproject backend
cd backend
python manage.py startapp users
```

**Bước 3:** Cấu hình settings.py
Mở backend/settings.py và thêm các cài đặt sau:

```sh
import os
from datetime import timedelta
from dotenv import load_dotenv
load_dotenv()

# Cấu hình ứng dụng
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    
    # Django REST Framework
    "rest_framework",
    "rest_framework_simplejwt",
    "corsheaders",

    # Ứng dụng Users
    "users",
]

# Cấu hình REST Framework
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
}

# Cấu hình JWT Token
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=1),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": True,
}

# Cấu hình MySQL
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": os.getenv("DB_NAME"),
        "USER": os.getenv("DB_USER"),
        "PASSWORD": os.getenv("DB_PASSWORD"),
        "HOST": os.getenv("DB_HOST", "localhost"),
        "PORT": os.getenv("DB_PORT", "3306"),
    }
}

# Cấu hình CORS để frontend (Streamlit) có thể gọi API
CORS_ALLOW_ALL_ORIGINS = True
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# Cấu hình Static files
STATIC_URL = "/static/"

SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_key")
DEBUG = os.getenv("DEBUG") == "True"
```

**Bước 4:** Tạo Model cho users
Mở users/models.py và tạo model cho User:

```sh
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=[("admin", "Admin"), ("user", "User")], default="user")
    
    def __str__(self):
        return self.username
```

📌 Lý do dùng AbstractUser: Django đã có sẵn hệ thống user, ta mở rộng nó bằng cách thêm email duy nhất và role.

**Bước 5:** Đăng ký Model trong admin.py
Mở users/admin.py:

```sh
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

admin.site.register(CustomUser, UserAdmin)
```

**Bước 6:** Cấu hình User Model trong settings.py
Thêm dòng này vào backend/settings.py để sử dụng CustomUser thay vì User mặc định:

```sh
AUTH_USER_MODEL = "users.CustomUser"
```

**Bước 7:** Tạo Serializer để trả về dữ liệu User
Tạo file users/serializers.py:

```sh
from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "role"]
```

**Bước 8:** Tạo View API cho Đăng ký, Đăng nhập
Mở users/views.py và tạo API:

```sh
from rest_framework import generics, permissions
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import UserSerializer

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        user = serializer.save()
        user.set_password(self.request.data["password"])
        user.save()

class CustomTokenObtainPairView(TokenObtainPairView):
    permission_classes = [permissions.AllowAny]

@api_view(["POST"])
def logout_view(request):
    try:
        refresh_token = request.data["refresh"]
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response({"message": "Logged out successfully."}, status=200)
    except Exception:
        return Response({"error": "Invalid token"}, status=400)
```

**Bước 9:** Tạo API Endpoint
Mở users/urls.py và thêm đường dẫn API:

```sh
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import RegisterView, CustomTokenObtainPairView, logout_view

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", CustomTokenObtainPairView.as_view(), name="login"),
    path("logout/", logout_view, name="logout"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
```

**Bước 10:** Cấu hình URL chính
Mở backend/urls.py và thêm API vào hệ thống:

```sh
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/users/", include("users.urls")),
]
```

**Bước 11:** Chạy Migration
Chạy lệnh để tạo database:

```sh
python manage.py makemigrations users
python manage.py migrate
```

Tạo siêu người dùng để đăng nhập admin:

```sh
python manage.py createsuperuser
```

**Bước 12:** Chạy Server Django
```sh
python manage.py runserver
```
📌 API Endpoint sẽ chạy tại:

Admin Panel: http://127.0.0.1:8000/admin/
Đăng ký: POST http://127.0.0.1:8000/api/users/register/
Đăng nhập: POST http://127.0.0.1:8000/api/users/login/
Đăng xuất: POST http://127.0.0.1:8000/api/users/logout/