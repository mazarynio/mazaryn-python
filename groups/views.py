
from friends.serializers import FriendSerializer
from .serializers import GroupSerializer
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Group


def ban(request, *args, **kwargs) -> Group.objects:
    member_id = request.data.get("members")
    group_name = request.data.get("group_name")
    if not member_id:
        return Response({"ban": False, "message": "Profile id is missing"})

    res = Group.objects.filter(member_id).update(banned_status=True)
    res.save()
    return Response({"banned": res, "message": member_id}, status=status.)


class GroupViewSet(viewsets.ModelViewSet):
    serializer_class = GroupSerializer
    queryset = Group.objects.all()









