from django.urls import path
from .views import my_profile_view, received_invites_view,profiles_list_view, invite_profiles_list_view

app_name = 'profiles'

urlpatterns = [
    path('', my_profile_view,name='my-profile-view'),
    path('my-invites/', received_invites_view, name = 'my-invites-view'),
    path('all-profiles/', profiles_list_view, name = 'all-profiles-view'),
    path('to-invite/', invite_profiles_list_view, name = 'to-invite-view'),
]