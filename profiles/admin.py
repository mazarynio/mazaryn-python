from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from .models import User, Profile
import logging


logger = logging.getLogger(__name__)


@admin.register(User)
class AdminUser(UserAdmin):
    '''
    Refactored django admin configuration to match up custom User model.
    Besides it returns a customized admin dashboard.
    '''
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
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("first_name", "slug")
    list_filter = ("slug", "created", "first_name")
    search_fields = ("first_name",)
    prepopulated_fields = {"slug": ("first_name",)}
    # autocomplete_fields = ("slug",)
    
    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return self.readonly_fields
        
        return list(self.readonly_fields) + ["slug", "first_name"]
    
    def get_prepopulated_fields(self, request, obj=None):
        if request.user.is_superuser:
            return self.prepopulated_fields
        else:
            return {}