from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Group



@receiver(pre_save, sender=Group)
def set_group_creator_admin_and_group_member(sender, instance, created, **kwargs):
    
    if created:
        instance.admin.add(*instance.created_by)
        instance.save()
        