from django.contrib import admin
from .models import Profile, Follow, Relationship


@admin.register(Profile)
class ProfileModel(admin.ModelAdmin):
    list_filter = ('slug', 'created', 'first_name')


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    model = Follow
    raw_id_fields = ("follower", "followee")


@admin.register(Relationship)
class RelationshipModel(admin.ModelAdmin):
    list_filter = ('status', 'created')
    list_display = ('sender', 'receiver', 'status')
