from django.db import models
from versatileimagefield.fields import VersatileImageField, PPOIField
import datetime
from django.utils import timezone



class PostImage(models.Model):
    '''
    This model handles a particular image(s) of a post and its full functionality is 
    backed by a third party package
    '''
    image = VersatileImageField('Image',upload_to='images/',ppoi_field='image_ppoi')
    image_ppoi = PPOIField()



class Post(models.Model):
    '''
    This class defines particulars of a post; post-related details such as author, 
    likes count alongside other features represented by the fields.
    Ordering of the post listing is from the most recent post downards as defined in the meta class.
    ''' 
    content = models.CharField(max_length=10000) 
    liked = models.ManyToManyField(
        "profiles.Profile", blank=True, related_name='post_likes')
    groups = models.ForeignKey(
        "groups.Group", blank=True, on_delete=models.SET_NULL, null=True, related_name='group_posts')
    image = models.ManyToManyField(PostImage,blank=True,related_name='posts_images')
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        "profiles.Profile", on_delete=models.CASCADE, null=True, related_name='posts')

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return str(f"{self.content[:40]}...")

    def no_of_likes(self):
        '''Returns likes count of a post'''
        return str(self.liked.all().count())

    def no_of_comments(self):
        '''Returns the comments count of a post'''
        return self.comment_set.all().count()

    @property
    def comments(self):
        return self.comment_set.all()
    
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    
class Comment(models.Model):
    '''
    This class defines particulars of a comment; comment-related details such as author, 
    likes count alongside other features represented by the fields.
    '''
    user = models.ForeignKey("profiles.Profile", on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    body = models.TextField(max_length=250)
    liked = models.ManyToManyField(
        "profiles.Profile", blank=True, related_name='comment_likes')
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    
    
    def no_of_likes(self):
        '''Returns likes count of a post'''
        return str(self.liked.all().count())

    def __str__(self):
        return str(self.pk)


LIKE_CHOICES = (
    ('Like', 'Like'),
    ('Unlike', 'Unlike'),
)


class Like(models.Model):
    '''
    This class represents the like object, all the related details such as the liker are defined.
    Ordering of likes follow same suit as in the comments and posts
    '''
    user = models.ForeignKey("profiles.Profile", on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    value = models.CharField(choices=LIKE_CHOICES, blank=True, max_length=8)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f"{self.user} - {self.post} - {self.value}"
