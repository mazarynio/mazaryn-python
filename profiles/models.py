from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.shortcuts import reverse
from django.db.models import Q
from django.db import models
from groups.models import Group
import profiles
import os


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
