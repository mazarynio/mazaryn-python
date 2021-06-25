import json
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.http import JsonResponse

from notifications.serializers import NotificationSerializer
from notifications.models import CustomNotification

from .models import Profile, Relationship, Follow, Block
from .serializers import BlockSerializer, FollowSerializer, ProfileSerializer,

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import UpdateAPIView
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, permission_classes, authentication_classes


@api_view(['POST', ])
@permission_classes([])
@authentication_classes([])
def send_friend_request(request, slug=None):
    if slug is not None:
        friend_user = Profile.objects.get(slug=slug)
        relationship = Relationship.objects.create(
            sender=request.user, receiver=friend_user, status='send')
        relationship.save()
        notification = CustomNotification.objects.create(
            type="friend", actor=request.user, recipient=friend_user, verb="Sent you friend request")
        channel_layer = get_channel_layer()
        channel = "notifications_{}".format(friend_user.username)
        async_to_sync(channel_layer.group_send)(
            channel, {
                "type": "notify",  # method name
                "command": "new_notification",
                "notification": json.dumps(NotificationSerializer(notification).data)
            }
        )
        data = {
            'status': True,
            'message': "Request sent"
        }
        return JsonResponse(data)


@api_view(['POST', ])
@permission_classes([])
@authentication_classes([])
def accept_friend_request(request, slug=None):
    if slug is not None:
        friend_user = Profile.objects.get(slug=slug)
        myself = request.user
        relationship = Relationship.objects.create(
            sender=slug, receiver=request.user, status="accepted")
        relationship.save()
        CustomNotification.objects.filter(
            recipient=myself, actor=friend_user).delete()
        data = {
            'status': True,
            'message': "You accepted friend request"
        }
        return JsonResponse(data)



class ReceivedInvitesList(generics.GenericAPIView, mixins.ListModelMixin):
    serializer_class = ProfileSerializer

    def get_queryset(self):
        profile = Profile.objects.get(user=self.request.user)
        queryset = Relationship.objects.invitations_received(profile)
        return queryset

    def get(self, request):
        return self.list(request)


class InvitesProfileList(generics.GenericAPIView, mixins.ListModelMixin):
    serializer_class = ProfileSerializer

    def get_queryset(self):
        sender = self.request.user
        queryset = Profile.objects.get_all_profiles_to_invite(sender)
        return queryset

    def get(self, request):
        return self.list(request)


class FriendsListView(generics.GenericAPIView, mixins.ListModelMixin):
    '''List this user's friends'''
    serializer_class = ProfileSerializer

    def get_queryset(self):
        current_friends = self.request.user.friends.all()

        return current_friends



class FollowersListView(generics.GenericAPIView, mixins.ListModelMixin):
    '''List this user's followers'''
    serializer_class = ProfileSerializer

    def get_queryset(self):
        user = self.request.user
        followers = Follow.objects.followers(user)

        return followers


class FollowingListView(generics.GenericAPIView, mixins.ListModelMixin):
    '''Lists who this current user instance follows'''
    serializer_class = ProfileSerializer

    def get_queryset(self):
        user = self.request.user
        following = Follow.objects.following(user)

        return following


@api_view(['POST', ])
def follower_add(request, followee_username):
    '''Create a following relationship'''
    followee = Profile.objects.get(username=followee_username)
    follower = request.user
    following = Follow.objects.add_follower(follower, followee)
    following.save()


@api_view(['POST', ])
def follower_remove(request, followee_username):
    '''Remove a following relationship'''
    followee = Profile.objects.get(username=followee_username)
    follower = request.user
    follow_status = Follow.objects.remove_follower(follower, followee)
    follow_status.save()

class BlockedListView(generics.GenericAPIView, mixins.ListModelMixin):
    '''List this user's blocklist'''
    serializer_class = BlockSerializer

    def get_queryset(self):
        user = self.request.user
        blocked = Block.objects.blocked(user)

        return blocked

class BlockingListView(generics.GenericAPIView, mixins.ListModelMixin):
    '''Lists who this current user can block'''
    serializer_class = BlockSerializer

    def get_queryset(self):
        user = self.request.user
        blocking = Block.objects.blocking(user)
        return blocking


@api_view(['POST', ])
def block_add(request, blockee_username):
    '''Create a blocking relationship relationship'''
    blockee = Profile.objects.get(username=blockee_username)
    blocker = request.user
    blocking = Block.objects.add_block(blockee, blocker)
    blocking.save()

@api_view(['POST', ])
def block_remove(request, blockee_username):
    '''Removing a blocking relationship relationship'''
    blockee = Profile.objects.get(username=blockee_username)
    blocker = request.user
    blocking = Block.objects.remove_block(blockee, blocker)
    blocking.save()

