from rest_framework import generics
from friendship.models import Friend, Follow, Block
from .serializers import BlockSerializer, FollowSerializer, FriendSerializer
from profiles.models import Profile
from friendship.models import FriendshipRequest

class SendFriendRequest(generics.CreateAPIView):
    other_user = Profile.objects.get(pk=2)
    Friend.objects.add_friend(request.user,  other_user,message='Hi! I would like to add you') 
class AcceptFriendRequest(generics.CreateAPIView):
    other_user = Profile.objects.get(pk=2)
    friend_request = FriendshipRequest.objects.get(from_user=request.user, to_user=other_user)
    friend_request.accept()   

class RemoveFriend(generics.CreateAPIView):
    other_user = Profile.objects.get(pk=2)
    Friend.objects.remove_friend(request.user, other_user)

class RejectFriendRequest(generics.CreateAPIView):
    other_user = Profile.objects.get(pk=2)
    friend_request = FriendshipRequest.objects.get(from_user=request.user, to_user=other_user)
    friend_request.reject()    
class FriendsList(generics.ListAPIView):
    '''List friends to the logged-in user instance'''
    
    serializer_class = FriendSerializer 
    def get_queryset(self):
        return Friend.objects.friends(self.request.user) 

class FriendShipRequests(generics.ListCreateAPIView):
    '''Lists friend requests received by a user '''
    
    serializer_class = FriendSerializer
    def get_queryset(self):
        return Friend.objects.unrejected_requests(user=self.request.user)

class RejectedFriendShipRequests(generics.ListAPIView):
    '''Lists friend requests received by a user '''
    
    serializer_class = FriendSerializer
    def get_queryset(self):
        return Friend.objects.rejected_requests(user=self.request.user)

class FollowersView(generics.ListAPIView):
    '''Lists followers to the logged-in user instance'''
   
    serializer_class = FollowSerializer
    def get_queryset(self):
        return Follow.objects.followers(self.request.user)
    
class Follow(generics.CreateAPIView):
    other_user = Profile.objects.get(pk=2)
    Follow.objects.add_follower(request.user, other_user)

class FollowingView(generics.ListCreateAPIView):
    '''Lists potential users to be followed by the logged-in user instance'''
    serializer_class = FollowSerializer
    def get_queryset(self):
        return Follow.objects.following(self.request.user)
class Block(generics.CreateAPIView):
    other_user = Profile.objects.get(pk=2)
    Block.objects.add_block(request.user, other_user)
    
class Unblock(generics.CreateAPIView):
    other_user = Profile.objects.get(pk=2)
    Block.objects.remove_block(request.user, other_user)
    
class BlockingView(generics.ListCreateAPIView):
    '''Lists potential users to be blocked by the logged-in user instance'''
    
    serializer_class = BlockSerializer
    def get_queryset(self):
        return Block.objects.blocking(self.request.user)

class BlockedView(generics.ListAPIView):
    '''Lists all blocked users to the logged-in user instance'''
    
    serializer_class = BlockSerializer
    def get_queryset(self):
        return Block.objects.blocked(self.request.user)