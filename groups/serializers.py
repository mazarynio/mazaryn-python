from rest_framework import serializers
from .models import Group


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'group_name', 'members',
                  'posts', 'created_by', 'created']
        depth = 1
        
        def create(self,validated_data):
            instance = super().create(validated_data)
            instance.admin.add(instance.created_by)
            instance.save()
            
            return instance
