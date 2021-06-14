from rest_framework import serializers
from profiles.models import Block, Profile, Follow, Relationship


class RegistrationSerializer(serializers.ModelSerializer):

    username = serializers.CharField(source='user.username')
    password = serializers.CharField(source='user.password')
    password2 = serializers.CharField(
        style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = Profile
        fields = ['email', 'username', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def save(self):
        profile = Profile(
            email=self.validated_data['email'], username=self.validated_data['username'])

        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError(
                {'password': 'Passwords do not match.'})

        profile.set_password(password)
        profile.save()
        return profile


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["id", "first_name", "last_name", "bio", "email", "avatar"]


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ["id", "follower", "followee"]
        

class BlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Block
        fields = ["id", "blocker", "blocked"]


class ChangePasswordSerializer(serializers.Serializer):

    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_new_password = serializers.CharField(required=True)


class RelationshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Relationship
        fields = "__all__"
