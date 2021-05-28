from .models import Profile, Relationship
from .serializers import ProfileSerializer

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, mixins, permissions


class MyProfileView(APIView):
    def get_object(self, user):
        try:
            return Profile.objects.get(user=self.request.user)
        except Profile.objects.DoesNotExist:
            return Response({"error": "The profile does not exist"}, status=404)

    def get(self, request, user=None):
        instance = self.get_object(user)
        serializer = ProfileSerializer(instance)
        return Response(serializer.data)


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


class ProfileListView(
    generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin
):
    serializer_class = ProfileSerializer

    def get_queryset(self):
        myself = self.request.user
        qs = Profile.objects.get_all_profiles(myself)
        return qs

    def get(self, request):
        return self.list(request)

    def post(self, request):
        return self.create(request)
