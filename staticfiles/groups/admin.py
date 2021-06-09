from django.contrib import admin
from .models import Group


@admin.register(Group)
class GroupModel(admin.ModelAdmin):
    list_filter = ('group_name', 'created', 'created_by')
    list_display = ('group_name', 'created')
