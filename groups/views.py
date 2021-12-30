
from .serializers import GroupSerializer
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Group, BanStatus
from profiles.models import Profile


def ban(self, request, *args, **kwargs):

    group_name = request.data.get("group_name")
    get_group = Group.objects.get(group_name=group_name)

    user_id = request.data.get("user_id")
    user = Profile.objects.get(id=user_id)

    if not user and not get_group:
        return Response({"message": "User or Group does not exist"},
                        status=status.HTTP_400_BAD_REQUEST)

    if get_group.get_members().filter(id=user_id) is not None:
        ban_status = BanStatus.objects.filter(group_name=get_group).update(status=True)
        ban_status.save()
        user.ban_status.add(ban_status)
        user.save()
        return Response(status=status.HTTP_200_OK)


class GroupViewSet(viewsets.ModelViewSet):
    serializer_class = GroupSerializer
    queryset = Group.objects.all()
