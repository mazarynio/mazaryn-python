from groups.serializers import GroupSerializer
from .models import Group
import logging
from rest_framework import viewsets


logger = logging.getLogger(__name__)


class GroupViewSet(viewsets.ModelViewSet):
    #Not yet worked on well especially logging aspect
    logger.info("Listing all groups...")

    serializer_class = GroupSerializer
    queryset = Group.objects.all()
