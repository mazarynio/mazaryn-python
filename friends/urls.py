from django.urls import path
from .views import *


urlpatterns = [
    
    path('all/',FriendsList.as_view()),
    path('send-request/', SendFriendRequest.as_view()),
    path('accept-request/', AcceptFriendRequest.as_view()),
    path('reject-request/', RejectFriendRequest.as_view()),
    path('remove-friend/', RemoveFriend.as_view()),
    path('requests/',FriendShipRequests.as_view()),
    path('rejected/',RejectedFriendShipRequests.as_view()),
    path('follow/', Follow.as_view()),
    path('followers/',FollowersView.as_view()),
    path('following/',FollowingView.as_view()),
    path('block/', Block.as_view()),
    path('blocking/',BlockingView.as_view()),
    path('blocked/',BlockedView.as_view()),
    path('unblock/', Unblock.as_view()),
    
]
