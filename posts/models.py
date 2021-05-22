from django.db import models
from django.core.validators import FileExtensionValidator


class Post(models.Model):
    content = models.TextField()
    image = models.ImageField(upload_to='posts', validators=[
                              FileExtensionValidator(['png', 'jpg', 'gif', 'jpeg'])], blank=True)
    liked = models.ManyToManyField(
        "profiles.Profile", blank=True, related_name='likes')
    groups = models.ForeignKey(
        "groups.Group", blank=True, on_delete=models.SET_NULL, null=True, related_name='group_posts')
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        "profiles.Profile", on_delete=models.CASCADE, related_name='posts')

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        # return str(self.pk)
        return str(f"{self.content[:40]}...")

    def no_of_likes(self):
        return str(self.liked.all().count())

    def no_of_comments(self):
        return self.comment_set.all().count()

    def get_group_posts(self):
        return

    @property
    def comments(self):
        return self.comment_set.all()


class Comment(models.Model):
    user = models.ForeignKey("profiles.Profile", on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    body = models.TextField(max_length=250)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.pk)


LIKE_CHOICES = (
    ('Like', 'Like'),
    ('Unlike', 'Unlike'),
)


class Like(models.Model):
    user = models.ForeignKey("profiles.Profile", on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    value = models.CharField(choices=LIKE_CHOICES, blank=True, max_length=8)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.post} - {self.value}"
