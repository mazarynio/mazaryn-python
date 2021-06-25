from django.contrib import admin
from .models import Profile


@admin.register(Profile)
class ProfileModel(admin.ModelAdmin):
    list_filter = ('slug', 'created', 'first_name')


