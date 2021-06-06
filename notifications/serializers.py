from rest_framework.serializers import ModelSerializer

from profiles.serializers import ProfileSerializer
from .models import CustomNotification

class NotificationSerializer(ModelSerializer):
    actor = ProfileSerializer(read_only=True)
    class Meta:
        model = CustomNotification
        fields = "__all__"
        
    