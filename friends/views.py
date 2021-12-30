from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import *
from .serializers import *
from profiles.models import Profile


###### --------Remove, list friends--------########

class FriendsList(generics.ListAPIView):
    '''
    List friends to the logged-in user instance
    '''
    serializer_class = FriendSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Friend.objects.friends(self.request.user)


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
        res = Friend.objects.remove_friend(self.request.user, profile.user)
        return Response({"unfriend": res, "message": None}, status=status.HTTP_204_NO_CONTENT)


###### --------Send, accept, reject and list friendrequests--------########

class SendFriendRequest(generics.CreateAPIView):
    """
    method:         POST
    HEADER:         Authorization: token <auth-token>
    request_data :  {"profile_id": int}
    """
    serializer_class = FriendSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        profile_id = request.data.get("profile_id")
        if not profile_id:
            return Response({"send": False, "message": "Profile id is missing"},
                            status=status.HTTP_400_BAD_REQUEST)
        profile = Profile.objects.get(id=profile_id)
        res = FriendshipRequest.objects.add_friend(self.request.user,
                                                   profile.user,
                                                   message='Hi! I would like to be your friend')
        return Response({"send": res, "message": None}, status=status.HTTP_201_CREATED)


class AcceptFriendRequest(generics.UpdateAPIView):
    """
    method:         POST
    HEADER:         Authorization: token <auth-token>
    request_data :  {"profile_id": int}
    """
    serializer_class = FriendSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def update(self, request, *args, **kwargs):
        profile_id = request.data.get("profile_id")
        if not profile_id:
            return Response({"accept": False, "message": "Profile id is missing"},
                            status=status.HTTP_400_BAD_REQUEST)
        profile = Profile.objects.get(id=profile_id)
        res = FriendshipRequest.objects.get(self.request.user,
                                            profile.user)
        res.accept()
        return Response({"accept": res, "message": None}, status=status.HTTP_201_CREATED)


class RejectFriendRequest(generics.DestroyAPIView):
    """
    method:         DELETE
    HEADER:         Authorization: token <auth-token>001caab988d3426760ba798a77f0c5081136cd2a
    request_data :  {"profile_id": int}
    """
    permission_classes = (permissions.IsAuthenticated,)

    def destroy(self, request, *args, **kwargs):
        profile_id = request.data.get("profile_id")
        if not profile_id:
            return Response({"reject": False, "message": "Profile is missing it might have been deleted/deactivated"},
                            status=status.HTTP_400_BAD_REQUEST)
        profile = Profile.objects.get(id=profile_id)
        res = FriendshipRequest.objects.get(self.request.user,
                                            profile.user)
        res.reject()
        return Response({"reject": res, "message": None}, status=status.HTTP_204_NO_CONTENT)


class FriendShipRequests(generics.ListCreateAPIView):
    '''
    Lists friend requests received by a user.
    '''
    serializer_class = FriendSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Friend.objects.unrejected_requests(user=self.request.user)


class RejectedFriendShipRequests(generics.ListAPIView):
    '''
    Lists friend requests received by a user.
    '''
    serializer_class = FriendSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Friend.objects.rejected_requests(user=self.request.user)


###### --------Follow, list followers--------########
class Follow(generics.CreateAPIView):
    """
    method:         POST
    HEADER:         Authorization: token <auth-token>
    request_data :  {"profile_id": int}
    """
    serializer_class = FollowSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        profile_id = request.data.get("profile_id")
        if not profile_id:
            return Response({"follow": False, "message": "Profile id missing to follow"},
                            status=status.HTTP_400_BAD_REQUEST)
        profile = Profile.objects.get(id=profile_id)
        res = Follow.objects.add_follower(self.request.user, profile.user)
        return Response({"follow": res, "message": None}, status=status.HTTP_201_CREATED)


class FollowersView(generics.ListAPIView):
    '''
    Lists followers to the logged-in user instance.
    '''
    serializer_class = FollowSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Follow.objects.followers(self.request.user)


class FollowingView(generics.ListCreateAPIView):
    '''
    Lists potential users to be followed by the logged-in user instance.
    '''
    serializer_class = FollowSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Follow.objects.following(self.request.user)


###### --------Block,Unblock and list blocked--------########

class Block(generics.CreateAPIView):
    """
    method:         POST
    HEADER:         Authorization: token <auth-token>
    request_data :  {"profile_id": int}
    """
    serializer_class = BlockSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        profile_id = request.data.get("profile_id")
        if not profile_id:
            return Response({"block": False, "message": "Profile id missing to block"},
                            status=status.HTTP_400_BAD_REQUEST)
        profile = Profile.objects.get(id=profile_id)
        res = Block.objects.add_block(self.request.user, profile.user)
        return Response({"block": res, "message": None}, status=status.HTTP_201_CREATED)


class Unblock(generics.DestroyAPIView):
    """
    method:         DELETE
    HEADER:         Authorization: token <auth-token>
    request_data :  {"profile_id": int}
    """
    permission_classes = (permissions.IsAuthenticated,)

    def destroy(self, request, *args, **kwargs):
        profile_id = request.data.get("profile_id")
        if not profile_id:
            return Response({"unblock": False, "message": "Profile id missing to unblock"},
                            status=status.HTTP_400_BAD_REQUEST)
        profile = Profile.objects.get(id=profile_id)
        res = Block.objects.remove_block(self.request.user, profile.user)
        return Response({"unblock": res, "message": None}, status=status.HTTP_204_NO_CONTENT)


class BlockingView(generics.ListCreateAPIView):
    '''
    Lists potential users to be blocked by the logged-in user instance.
    '''
    serializer_class = BlockSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Block.objects.blocking(self.request.user)


class BlockedView(generics.ListAPIView):
    '''
    Lists all blocked users to the logged-in user instance.
    '''
    serializer_class = BlockSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Block.objects.blocked(self.request.user)
