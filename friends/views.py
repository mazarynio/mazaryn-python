from rest_framework import viewsets
from friendship.models import Friend, Follow, Block
from .serializers import BlockSerializer, FollowSerializer, FriendSerializer

class FriendViewSet(viewsets.ReadOnlyModelViewSet):
    '''List this user's friends'''
    serializer_class = FriendSerializer
    def get_queryset(self):
        return Friend.objects.friends(self.request.user)

class UnreadFriendShipViewSet(viewsets.ModelViewSet):
    serializer_class = FriendSerializer
    def get_queryset(self):
        return Friend.objects.unread_requests(user=self.request.user)

class FriendShipRequestViewSet(viewsets.ModelViewSet):
    serializer_class = FriendSerializer
    def get_queryset(self):
        return Friend.objects.unrejected_requests(user=self.request.user)

class FriendShipRequestCountViewSet(viewsets.ModelViewSet):
    serializer_class = FriendSerializer
    def get_queryset(self):
        return Friend.objects.unrejected_request_count(user=self.request.user)

class RejectedFriendShipRequests(viewsets.ModelViewSet):
    serializer_class = FriendSerializer
    def get_queryset(self):
        return Friend.objects.rejected_requests(user=self.request.user)

class RejectedFriendShipRequestCount(viewsets.ModelViewSet):
    serializer_class = FriendSerializer
    def get_queryset(self):
        return Friend.objects.rejected_request_count(user=self.request.user)

class SentFriendShip(viewsets.ModelViewSet):
    serializer_class = FriendSerializer
    def get_queryset(self):
        return Friend.objects.sent_requests(user=self.request.user)

class FriendShipTest(viewsets.ModelViewSet):
    serializer_class = FriendSerializer
    def get_queryset(self):
        return Friend.objects.are_friends(self.request.user, other_user) == True


class FollowersViewSet(viewsets.ModelViewSet):
    serializer_class = FollowSerializer
    def get_queryset(self):
        return Follow.objects.followers(self.request.user)
    
class FollowingViewSet(viewsets.ModelViewSet):
    serializer_class = FollowSerializer
    def get_queryset(self):
        return Follow.objects.following(self.request.user)


class BlockingViewSet(viewsets.ModelViewSet):
    serializer_class = BlockSerializer
    def get_queryset(self):
        return Block.objects.blocking(self.request.user)


class BlockedViewSet(viewsets.ModelViewSet):
    serializer_class = BlockSerializer
    def get_queryset(self):
        return Block.objects.blocked(self.request.user)
    
    
class BlockedTest(viewsets.ModelViewSet):
    serializer_class = BlockSerializer
    def get_queryset(self):
        return Block.objects.is_blocked(self.request.user, other_user) == True
