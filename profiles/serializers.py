from rest_framework import serializers
from profiles.models import Profile



class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["id", "first_name", "last_name", "bio", "email", "avatar"]