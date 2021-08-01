from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from .models import Relationship


@receiver(post_save, sender=Relationship)
def post_save_add_friends(sender, instance, created, **kwargs):
    '''Invoked when the relationship status is accepted thus adding friends'''
    if instance.status == "accepted":
        sender_ = instance.sender
        receiver_ = instance.receiver

        sender_.friends.add(receiver_.user)
        receiver_.friends.add(sender_.user)
        sender_.save()
        receiver_.save()


@receiver(pre_delete, sender=Relationship)
def pre_delete_remove_from_friends(sender, instance, **kwargs):
    '''Removes a friend from the friends list'''
    sender = instance.sender
    receiver = instance.receiver
    sender.friends.remove(receiver.user)
    receiver.friends.remove(sender.user)
    sender.save()
    receiver.save()
