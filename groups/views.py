from .serializers import GroupSerializer
from rest_framework import viewsets
from .models import Group


class GroupViewSet(viewsets.ModelViewSet):
    serializer_class = GroupSerializer
    queryset = Group.objects.all()
    

