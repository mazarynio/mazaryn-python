from rest_framework import fields
from rest_framework.serializers import ModelSerializer
from profiles.models import Profile


class RegistrationSerializer(ModelSerializer):

    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'email', ]
