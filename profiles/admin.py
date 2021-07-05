from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from .models import User, Profile


@admin.register(User)
class AdminUser(UserAdmin):
    '''Refactored django admin configuration to match up custom User model.'''
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            "Personal info",
            {"fields": ("first_name", "last_name")},
        ),
        (
            "Permissions", {"fields": (
                "is_active",
                "is_staff",
                "is_superuser",
                "groups",
                "user_permissions",
            )},
        ),
        (
            "Important dates",
            {"fields": ("last_login", "date_joined")},
        )
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "password1", "password2"),
        },
        )
    )
    list_display = (
        "email",
        "first_name",
        "last_name",
        "is_staff",
        "is_superuser",
    )
    search_fields = ("email", "first_name", "last_name")
    ordering = ("email",)


@admin.register(Profile)
class ProfileModel(admin.ModelAdmin):
    list_filter = ('slug', 'created', 'first_name')
