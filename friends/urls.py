from django.urls import path
from .views import *


urlpatterns = [
    
    path('all/',FriendsList.as_view()),
    path('rejected/',RejectedFriendShipRequests.as_view()),
    path('requests/',FriendShipRequests.as_view()),
    path('rejected/',RejectedFriendShipRequests.as_view()),
    path('followers/',FollowersView.as_view()),
    path('follow/',FollowingView.as_view()),
    path('block/',BlockingView.as_view()),
    path('blocked/',BlockedView.as_view()),
    
]
