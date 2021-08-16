import logging
from .models import Group
from rest_framework import serializers

logger = logging.getLogger(__name__)

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'group_name', 'admin','members',
                  'posts', 'created_by', 'created']
        depth = 1
    
    def create(self,validated_data):
        logger.info(" \n ========== \n Creating a new group...\n ========= \n New group created \n **********")
        
        instance = super().create(validated_data)
        request = self.context['request']
        
        instance.admin.add(request.user.profile)
        instance.created_by = request.user.profile
        instance.save()
        instance.members.add(request.user.profile)
        return instance