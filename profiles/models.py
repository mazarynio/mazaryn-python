from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.shortcuts import reverse
from django.db.models import Q
from django.db import models
from groups.models import Group
import profiles
import os
from django.core.exceptions import ValidationError
from django.utils import timezone


class ProfileManager(models.Manager):

    def get_all_profiles(self, myself):
        profiles = Profile.objects.all().exclude(user=myself)
        return profiles

    def get_all_profiles_to_invite(self, myself):
        profiles = Profile.objects.all().exclude(user=myself)
        profile = Profile.objects.get(user=myself)
        qs = Relationship.objects.filter(
            Q(sender=profile) | Q(receiver=profile))
        accepted_invitations = []
        for relationship in qs:
            if relationship.status == 'accepted':
                accepted_invitations.append(relationship.receiver)
                accepted_invitations.append(relationship.sender)

        available = [
            profile for profile in profiles if profile not in accepted_invitations]
        return available


def upload_avatar(instance, filename):
    path = 'avatars'
    ext = filename.split('.')[-1]
    filename = '{}.{}'.format(instance.user.username, ext)
    return os.path.join(path, filename)


class Profile(models.Model):
    '''Returns more details about a registered user, it extends the default **User model '''
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=200, blank=True)
    last_name = models.CharField(max_length=200, blank=True)
    bio = models.TextField(default='No bio...', max_length=300, blank=True)
    email = models.EmailField(max_length=200, blank=True)
    country = models.CharField(max_length=200, blank=True)
    avatar = models.ImageField(default='avatar.png', upload_to=upload_avatar)
    friends = models.ManyToManyField(User, blank=True, related_name='friends')
    groups = models.ManyToManyField(Group, blank=True)

    slug = models.SlugField(unique=True, blank=True)
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now_add=True)

    objects = ProfileManager()

    def absolute_profile_url(self):
        return reverse('profiles:profile-detail-view', kwargs={"slug": self.slug})

    def get_friends(self):
        return self.friends.all()

    def get_friends_no(self):
        return self.friends.all().count()

    def get_posts_no(self):
        return self.posts.all().count()

    def get_all_author_posts(self):
        return self.posts.all()

    def get_no_of_likes_given(self):
        likes = self.like_set.all()
        total_liked = 0
        for item in likes:
            if item.value == 'Like':
                total_liked += 1
        return total_liked

    def get_no_of_likes_received(self):
        '''Dropped the syntax model_set because of the related name in the model Post.'''
        posts = self.posts.all()
        total_liked = 0
        for item in posts:
            total_liked += item.liked.all().count()
        return total_liked

    def __str__(self):
        return f"{self.user.username}"

    intial_first_name = None
    intial_last_name = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.intial_first_name = self.first_name
        self.intial_last_name = self.last_name

    def save(self, *args, **kwargs):
        ex = False
        to_slug = self.slug
        if self.first_name != self.intial_first_name or self.last_name != self.intial_last_name or self.slug == "":
            if self.first_name and self.last_name:
                to_slug = slugify(str(self.first_name) +
                                  '_' + str(self.last_name))
                ex = Profile.objects.filter(slug=to_slug).exists()
                while ex:
                    to_slug = slugify(
                        to_slug + '-' + str(profiles.get_random_code()))
                    ex = Profile.objects.filter(slug=to_slug).exists()
            else:
                to_slug = str(self.user)
        self.slug = to_slug
        super().save(*args, **kwargs)


class RelationshipManager(models.Manager):
    def invitations_received(self, receiver):
        rlnshp_query_set = Relationship.objects.filter(
            receiver=receiver, status='send')
        return rlnshp_query_set


STATUS_CHOICES = [
    ('send', 'send'),
    ('accepted', 'accepted')
]


class Relationship(models.Model):
    sender = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name='receiver')
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
        followers = [p.follower for p in qs]

        return followers

    def following(self, user):
        '''Return a list of all users the given user follows '''
        qs = Follow.objects.filter(follower=user).all()
        following = [p.followee for p in qs]

        return following

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
        if followers and followee in followers:
            return True

        elif following and follower in following:
            return True

        else:
            return Follow.objects.filter(follower=follower, followee=followee).exists()


class Follow(models.Model):
    """Model to represent Following relationships"""

    follower = models.ForeignKey(
        User, models.CASCADE, related_name='following')
    followee = models.ForeignKey(
        User, models.CASCADE, related_name='followers')
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
        blocked = [u.blocked for u in qs]
        return blocked

    def blocking(self, user):
        """ Return a list of all users the given user could blocks """
        qs = Block.objects.filter(blocker=user).all()
        blocking = [u.blocked for u in qs]
        return blocking

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
    blocker = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='blocking')
    blocked = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='blockees')
    created = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.blocker} has blocked {self.blocked}."

    def save(self, *args, **kwargs):
        # Ensures users can't block themselves
        if self.blocker == self.blocked:
            raise ValidationError('You cannot block yourself!')
        super().save(*args, **kwargs)
    
    
    