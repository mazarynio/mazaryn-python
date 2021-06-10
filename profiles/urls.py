from django.urls import path
from .views import (  # ReceivedInvitesList, ProfileListView, MyProfileView, InvitesProfileList,
    # registration_view, LoginView, update_profile_view, does_account_exist_view, ChangePasswordView,
    FriendsListView, send_friend_request, accept_friend_request, follower_add, follower_remove, FollowersListView,
    FollowingListView)

urlpatterns = [
    #     path('check_if_account_exists/', does_account_exist_view,
    #          name='check_if account_exists'),
    #     path('login/', LoginView.as_view(), name='login'),
    #     path('register/', registration_view, name='register'),
    #     path('myprofile/', MyProfileView.as_view()),
    #     path('myprofile/update/', update_profile_view, name='update_profile'),
    #     path('myprofile/change_password/',
    #          ChangePasswordView.as_view(), name='change_password'),
    #     path('all_profiles/', ProfileListView.as_view()),
    path('friends/', FriendsListView.as_view(), name='friends'),
    #     path('myprofile/my-invites/', ReceivedInvitesList.as_view()),
    #     path('myprofile/to-invite/', InvitesProfileList.as_view()),
    path('send_request/<slug:slug>/', send_friend_request, name='send-request'),
    path('accept_request/<slug:slug>/',
         accept_friend_request, name='accept-request'),
    path('myprofile/followers/', FollowersListView.as_view(), name='followers'),
    path('myprofile/following/', FollowingListView.as_view(), name='following'),
    path('all_profiles/follower_add/', follower_add, name='add_follower'),
    path('all_profiles/follower_remove/',
         follower_remove, name='remove_follower'),


]
