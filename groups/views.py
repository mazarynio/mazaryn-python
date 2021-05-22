from groups.serializers import GroupSerializer
from .models import Group

from rest_framework import viewsets


class GroupViewSet(viewsets.ModelViewSet):
    serializer_class = GroupSerializer
    queryset = Group.objects.all()
