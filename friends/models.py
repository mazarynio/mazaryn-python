from django.db import models
import profiles
from django.core.exceptions import ValidationError
from django.utils import timezone


class RelationshipManager(models.Manager):
    def invitations_received(self, receiver):
        return Relationship.objects.filter(
            receiver=receiver, status='send')


STATUS_CHOICES = [
    ('send', 'send'),
    ('accepted', 'accepted')
]

class Relationship(models.Model):
    sender = models.ForeignKey(
        'profiles.Profile', on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(
        'profiles.Profile', on_delete=models.CASCADE, related_name='receiver')
    status = models.CharField(max_length=8, choices=STATUS_CHOICES)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    objects = RelationshipManager()

    def __str__(self):
        return f"{self.sender} - {self.receiver} - {self.status} was initiated {self.created.strftime('%d-%m-%y')}"


class FollowManager(models.Manager):
    '''Following manager'''

    def followers(self, user):
        '''Returns list of all followers'''
        qs = Follow.objects.filter(followee=user).all()
        return [p.follower for p in qs] 

    def following(self, user):
        '''Return a list of all users the given user follows '''
        qs = Follow.objects.filter(follower=user).all()
        return [p.followee for p in qs] 

    def add_follower(self, follower, followee):
        """Create's 'follower' follows 'followee' relationship"""
        if follower == followee:
            raise ValidationError('You cannot follow yourself')

        status, created = Follow.objects.get_or_create(
            follower=follower, followee=followee)

        if created is False:
            raise ValidationError(f"{follower} already follows {followee}")

        return status

    def remove_follower(self, follower, followee):
        """ Remove 'follower' follows 'followee' relationship """
        try:
            status = Follow.objects.get(follower=follower, followee=followee)
            status.delete()

        except Follow.DoesNotExist:
            raise ValidationError('This relationship does not exist')

    def follows(self, follower, followee):
        """ Does follower follow followee?"""
        if (
            followers
            and followee in followers
            or following
            and follower in following
        ):
            return True

        else:
            return Follow.objects.filter(follower=follower, followee=followee).exists()


class Follow(models.Model):
    """Model to represent Following relationships"""

    follower = models.ForeignKey(
        'profiles.Profile', models.CASCADE, related_name='following')
    followee = models.ForeignKey(
        'profiles.Profile', models.CASCADE, related_name='followers')
    created = models.DateTimeField(default=timezone.now)

    objects = FollowManager()

    def __str__(self):
        return f"{self.follower} follows {self.followee}"

    def save(self, *args, **kwargs):
        # Ensures users can't be friends with themselves
        if self.follower == self.followee:
            raise ValidationError('You cannot follow yourself')
        super().save(*args, **kwargs)
        
        
class BlockManager(models.Manager):
    """ Blocking manager """

    def blocked(self, user):
        """ Return a list of all blocked  """
        qs = Block.objects.filter(blocked=user).all()
        return [u.blocked for u in qs]

    def blocking(self, user):
        """ Return a list of all users the given user could blocks """
        qs = Block.objects.filter(blocker=user).all()
        return [u.blocked for u in qs]

    def add_block(self, blocker, blocked):
        """ Create 'blocker' blocks 'blocked' relationship """
        if blocker == blocked:
            raise ValidationError("Users cannot block themselves")

        relation, created = Block.objects.get_or_create(
            blocker=blocker, blocked=blocked
        )

        if created is False:
            raise ValidationError(
                f"{self.blocker} has already blocked {self.blocked}"
            )

        return relation

    def remove_block(self, blocker, blocked):
        """ Remove 'blocker' blocks 'blocked' relationship """
        try:
            rel = Block.objects.get(blocker=blocker, blocked=blocked)
            rel.delete()
            return True
        except Block.DoesNotExist:
            return False

class Block(models.Model):
    '''Model representing blocking relationships'''
    blocker = models.ForeignKey('profiles.Profile', on_delete=models.CASCADE, related_name='blocking')
    blocked = models.ForeignKey('profiles.Profile', on_delete=models.CASCADE, related_name='blockees')
    created = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.blocker} has blocked {self.blocked}."

    def save(self, *args, **kwargs):
        # Ensures users can't block themselves
        if self.blocker == self.blocked:
            raise ValidationError('You cannot block yourself!')
        super().save(*args, **kwargs)
    
    
    
