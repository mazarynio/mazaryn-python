from django.urls import path
from .views import (ReceivedInvitesList, ProfileListView, MyProfileView, InvitesProfileList,
                    registration_view, LoginView, update_profile_view, does_account_exist_view, ChangePasswordView)

urlpatterns = [
    path('check_if_account_exists/', does_account_exist_view,
         name='check_if account_exists'),
    path('login/', LoginView.as_view(), name='login'),
    path('register/', registration_view, name='register'),
    path('myprofile/', MyProfileView.as_view()),
    path('myprofile/update/', update_profile_view, name='update_profile'),
    path('myprofile/change_password/',
         ChangePasswordView.as_view(), name='change_password'),
    path('all_profiles/', ProfileListView.as_view()),
    path('myprofile/my-invites/', ReceivedInvitesList.as_view()),
    path('myprofile/to-invite/', InvitesProfileList.as_view()),

]
