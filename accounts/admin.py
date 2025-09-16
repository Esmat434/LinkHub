from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    CustomUser,ForgotPassword
)
# Register your models here.

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {"fields": ("username", "email", "slug")}),
        ("Personal info", {"fields": ("first_name", "last_name", "avatar", "password")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "email_verified",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "email", "slug", "usable_password", "password1", "password2"),
            },
        ),
    )
    list_display = ['username','slug','email','first_name','last_name','is_superuser']

@admin.register(ForgotPassword)
class TokenAdmin(admin.ModelAdmin):
    list_display = ['user','token','created_at']