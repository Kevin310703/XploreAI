from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from .models import CustomUser

# Register your models here.
class UserAdmin(UserAdmin):
    list_display = ("username", "email", "avatar_preview")
    readonly_fields = ("avatar_preview",)

    fieldsets = (
        ("Personal Info", {
            "fields": ("username", "email", "first_name", "last_name", "avatar", "avatar_preview"),
        }),
        ("Password", {
            "fields": ("password",),
        }),
        ("Permissions", {
            "fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions"),
        }),
        ("Important Dates", {
            "fields": ("last_login", "date_joined"),
        }),
    )

    def avatar_preview(self, obj):
        """Display avatar in admin panel."""
        if obj.avatar:
            return format_html('<img src="{}" width="80" style="border-radius: 10px; border: 1px solid #ccc;" />', obj.avatar.url)
        return "No Avatar"

    avatar_preview.short_description = "Avatar Preview"

admin.site.register(CustomUser, UserAdmin)