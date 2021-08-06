from rest_framework import serializers
from .models import Group


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'group_name', 'admin','members',
                  'posts', 'created_by', 'created']
        depth = 1
    
    def create(self,validated_data):
        instance = super().create(validated_data)
        request = self.context['request']
        instance.admin = request.user.profile
        instance.save()
        instance.members.add(request.user.profile)
        return instance