from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import User, Profile
from rest_framework.authtoken.models import Token
import logging

logger = logging.getLogger(__name__)


@receiver(post_save, sender=User)
def post_save_create_profile(sender, instance, created, **kwargs):

    logger.info('Profile for the new user created')
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def set_new_user_active(sender, instance, created=True, **kwargs):
    if created:
        instance.is_active = True


@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
