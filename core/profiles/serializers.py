from rest_framework import serializers
from .models import Profile , Relationship

class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Profile
        fields = ['url','first_name','last_name','bio','email','avatar',]


class RelationshipSerializer(serializers.HyperlinkedModelSerializer):
    class META:
        model = Relationship
        fields = '__all__'