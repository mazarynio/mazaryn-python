import uuid
from django.db import models
from profiles.models import Profile

class Room(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='author_room')
    friend = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='friend_room')

class Message(models.Model):
    message = models.TextField()
    room = models.ForeignKey(Room, on_delete=models.DO_NOTHING, related_name='messages')
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='author_messages')
    friend = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='friend_messages')
    
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message + " " + str(self.timestamp)

