from django.db import models
from django.template.defaultfilters import default
from django.utils import timezone


#  using django  groups


class Group(models.Model):
    group_name = models.CharField(max_length=200, blank=True, unique=True)
    description = models.TextField(
        help_text='Describe this group...', max_length=350, blank=True)
    admin = models.ManyToManyField(
        "profiles.Profile", blank=True, related_name='group_admin')
    members = models.ManyToManyField(
        "profiles.Profile", blank=True, related_name='members')

    posts = models.ForeignKey(
        "posts.Post", blank=True, on_delete=models.SET_NULL, null=True, related_name='group_posts')
    created_by = models.ForeignKey(
        "profiles.Profile", on_delete=models.SET_NULL, null=True, related_name='group_creator')
    created = models.DateTimeField(auto_now=True)

    def get_members(self):
        return self.members.all()

    def get_members_no(self):
        return self.friends.all().count()

    def get_group_posts(self):
        return self.group_posts.all()

    def get_group_posts_no(self):
        return self.group_posts.all().count()

    def get_group_creator(self):
        return self.created_by.user

    def get_admins(self):
        return self.admin.all()

    def get_admins_count(self):
        return self.admin.all().count()

    def __str__(self):
        return f"{self.group_name}"


class BanStatus(models.Model):
    """

    """
    group_name = models.OneToOneField(Group, on_delete=models.CASCADE)
    ban_status = models.BooleanField(default=False)
    ban_date = models.DateTimeField(auto_now=True)
