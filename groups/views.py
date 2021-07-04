from groups.serializers import GroupSerializer
from .models import Group
import logging
from rest_framework import viewsets


logger = logging.getLogger(__name__)


class GroupViewSet(viewsets.ModelViewSet):
    logger.info("Listing all groups...")

    serializer_class = GroupSerializer
    queryset = Group.objects.all()
