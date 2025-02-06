from django.db import models
from django.contrib.auth.models import AbstractUser
from .utils.helper import user_avatar_upload_path

# Create your models here.
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=[("admin", "Admin"), ("user", "User")], default="user")
    avatar = models.ImageField(upload_to=user_avatar_upload_path, default="avatars/default_avatar.jpg", null=True, blank=True)

    def __str__(self):
        return self.username