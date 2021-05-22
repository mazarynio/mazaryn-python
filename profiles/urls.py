from django.urls import path
from .views import (ReceivedInvitesList, ProfileListView,
                    MyProfileView, InvitesProfileList)

urlpatterns = [
    path('', ProfileListView.as_view()),
    path('myprofile/', MyProfileView.as_view()),
    path('myprofile/my-invites/', ReceivedInvitesList.as_view()),
    path('myprofile/to-invite/', InvitesProfileList.as_view()),

]
