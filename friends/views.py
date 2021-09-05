from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework import status
from friends.models import Friend, Follow, Block, FriendshipRequest
from .serializers import BlockSerializer, FollowSerializer, FriendSerializer
from profiles.models import Profile


class RemoveFriend(generics.DestroyAPIView):
    """
    method:         DELETE
    HEADER:         Authorization: token <auth-token>001caab988d3426760ba798a77f0c5081136cd2a
    request_data :  {"profile_id": int}
    """
    permission_classes = (permissions.IsAuthenticated,)

    def destroy(self, request, *args, **kwargs):
        profile_id = request.data.get("profile_id")
        if not profile_id:
            return Response({"unfriend": False, "message": "Profile id missing to unfriend user"},
                            status=status.HTTP_400_BAD_REQUEST)
        profile = Profile.objects.get(id=profile_id)
        res = Friend.objects.remove_friend(request.user, profile.user)
        return Response({"unfriend": res, "message": None}, status=status.HTTP_200_OK)



class SendFriendRequest(generics.CreateAPIView):
    other_user = Profile.objects.get(pk=2)
    Friend.objects.add_friend(request.user,  other_user,message='Hi! I would like to add you')
class AcceptFriendRequest(generics.CreateAPIView):
    other_user = Profile.objects.get(pk=2)
    friend_request = FriendshipRequest.objects.get(from_user=request.user, to_user=other_user)
    friend_request.accept()   

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