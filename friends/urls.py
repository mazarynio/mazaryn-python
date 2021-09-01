from django.urls import path, include
from .views import *
from rest_framework import routers


router = routers.DefaultRouter()

router.register('', FriendViewSet, basename='Friend')
router.register('unread', UnreadFriendShipViewSet, basename='Friend')
router.register('requests', FriendShipRequestViewSet, basename='Friend')
router.register('', FriendShipRequestCountViewSet, basename='Friend')
router.register('rejected', RejectedFriendShipRequests, basename='Friend')
router.register('', RejectedFriendShipRequestCount, basename='Friend')
router.register('sent-requests', SentFriendShip, basename='Friend')
router.register('', FriendShipTest, basename='Friend')
router.register('followers', FollowersViewSet, basename='Friend')
router.register('following', FollowingViewSet, basename='Friend')
router.register('blocking', BlockingViewSet, basename='Friend')
router.register('blocked', BlockedViewSet, basename='Friend')
router.register('', BlockedTest, basename='Friend')


urlpatterns = [
    path('', include(router.urls)),
]
