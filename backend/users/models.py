import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from .utils.helper import user_avatar_upload_path

# Create your models here.
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    is_email_verified = models.BooleanField(default=False)
    email_verification_token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    role = models.CharField(max_length=20, choices=[("admin", "Admin"), ("user", "User")], default="user")
    avatar = models.ImageField(upload_to=user_avatar_upload_path, default="avatars/default_avatar.jpg", null=True, blank=True)

    def generate_new_verification_token(self):
        """Tạo token xác nhận email mới"""
        self.email_verification_token = uuid.uuid4()
        self.save()

    def __str__(self):
        return self.username