from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.db.models import Q
from django.db import models
from groups.models import Group
import profiles
import os
from friends.models import Relationship


class UserManager(BaseUserManager):
    '''This manager class inherits its core functionality
    from django's BaseUserManager to extend it to User class'''
    use_in_migrations = True

    # Due to the conflicting syntax the naming takes underscore to differentiate them
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_staff", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        if extra_fields.get("is_staff") is not True:
            raise ValueError(
                "Superuser must have is_staff set to True."
            )
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(
                "Superuser must have is_superuser set to True."
            )
        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    '''Custom user model for handling details required for Registration, Login.
    Besides this model sets attributes such as active and superuser statuses.
    This model defaults email as a required field.'''
    username = None
    email = models.EmailField('email address', unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()


class ProfileManager(models.Manager):
    '''Extends the profile class default **Objects** manager by appending subsequent methods.'''

    def get_all_profiles(self, myself):
        '''Lists all profiles to the user excluding the logged in user instance from the list.'''
        return Profile.objects.all().exclude(user=myself)

    def get_all_profiles_to_invite(self, myself):
        '''Returns all profiles eligible for relationship to be initiated, the method excludes the following 
        from the list: 
        1.Instance of the current user logged in
        2.Current friends
        3.Instances where the status of the relationship is **-sent** (awaiting for acceptance)'''
        profiles = Profile.objects.all().exclude(user=myself)
        profile = Profile.objects.get(user=myself)
        qs = Relationship.objects.filter(
            Q(sender=profile) | Q(receiver=profile))
        accepted_invitations = []
        for relationship in qs:
            if relationship.status == 'accepted':
                accepted_invitations.append(relationship.receiver)
                accepted_invitations.append(relationship.sender)

        return [
            profile for profile in profiles if profile not in accepted_invitations]


def upload_avatar(instance, filename):
    '''Handles avatar upload.
    This is function handles the user uploaded avatars '''
    path = 'avatars'
    ext = filename.split('.')[-1]
    filename = '{}.{}'.format(instance.user.username, ext)
    return os.path.join(path, filename)


class Profile(models.Model):
    '''Returns refined details about a registered user, it extends the default **User model '''
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

    def get_friends(self):
        '''This method queries the database of all friends of the current logged in user.'''
        return self.friends.all()

    def get_friends_no(self):
        '''Returns the number of the friends total.'''
        return self.friends.all().count()

    def get_posts_no(self):
        '''Returns the total number of posts of a user.'''
        return self.posts.all().count()

    def get_all_author_posts(self):
        '''Returns a list of posts of a user.'''
        return self.posts.all()

    def get_no_of_likes_given(self):
        '''Reurns the count of likes of a user.'''
        likes = self.like_set.all()
        return sum(item.value == 'Like' for item in likes)

    def get_no_of_likes_received(self):
        '''Returns the count of likes from a user's total posts'''
        posts = self.posts.all()
        return sum(item.liked.all().count() for item in posts)

    def __str__(self):
        return f"{self.user.email}"

    intial_first_name = None
    intial_last_name = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.intial_first_name = self.first_name
        self.intial_last_name = self.last_name

    def save(self, *args, **kwargs):
        '''This function overides the default save() method available for models.
        This function generates the slug based on:
        1. If first and last names are provided then slug will be generated from them.
        2. Does check on the availability of a slug and ensures that the unique slug is not
        changed each and everytime the profile is updated.'''
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
