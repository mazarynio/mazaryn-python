from django.db import models
from django.utils.timezone import now
from profiles.models import Profile


class CustomNotification(models.Model):
    type = models.CharField(default='friend', max_length=30)
    recipient = models.ForeignKey(Profile, blank=False, on_delete=models.CASCADE, related_name='notifications')
    unread = models.BooleanField(default=True, blank=False, db_index=True)
    actor = models.ForeignKey(Profile, blank=False, on_delete=models.CASCADE)
    verb = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(default=now, db_index=True)
    deleted = models.BooleanField(default=False, db_index=True)
    emailed = models.BooleanField(default=False, db_index=True)
