from django.urls import path, include
from .views import *
from rest_framework import routers


router = routers.DefaultRouter()

router.register('', FriendViewSet)
router.register('', UnreadFriendShipViewSet)
router.register('', FriendShipRequestViewSet)
router.register('', FriendShipRequestCountViewSet)
router.register('', RejectedFriendShipRequests)
router.register('', RejectedFriendShipRequestCount)
router.register('', SentFriendShip)
router.register('', FriendShipTest)
router.register('', FollowersViewSet)
router.register('', FollowingViewSet)
router.register('', BlockingViewSet)
router.register('', BlockedViewSet)
router.register('', BlockedTest)


urlpatterns = [
    path('', include(router.urls)),
]
