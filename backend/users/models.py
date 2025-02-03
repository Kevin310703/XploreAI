from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=[("admin", "Admin"), ("user", "User")], default="user")
    
    def __str__(self):
        return self.username