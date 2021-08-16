from django.core import validators
import posts
from django.db import models
from django.core.validators import FileExtensionValidator
# from django.template.defaultfilters import slugify
# from profiles.utils import get_random_code

class Post(models.Model):
    '''This class defines particulars of a post; post-related details such as author, 
    likes count alongside other features represnted by the fields.
    Ordering of the post listing is from the most recent post downards as defined in the meta class.'''
    
    # title = models.CharField(max_length=50, blank=True)
    content = models.TextField() 
    liked = models.ManyToManyField(
        "profiles.Profile", blank=True, related_name='post_likes')
    groups = models.ForeignKey(
        "groups.Group", blank=True, on_delete=models.SET_NULL, null=True, related_name='group_posts')
    # slug = models.SlugField(max_length=50, unique=True, null=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        "profiles.Profile", on_delete=models.CASCADE, related_name='posts')

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
    
    
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.intial_title = self.title
        
    # def save(self, *args, **kwargs):
    #     '''This function overides the default save() method available for post.
    #     This function generates the slug based on:
    #     1. If post title is provided then slug will be generated from them.
    #     2. Does check on the availability of a slug and ensures that the unique slug is not
    #     changed each and everytime the post is updated.'''
    #     ex = False
    #     to_slug = self.slug
    #     if self.title != self.intial_title or self.slug == "":
    #         if self.title:
    #             to_slug = slugify(str(self.title))
    #             ex = Post.objects.filter(slug=to_slug).exists()
    #             while ex:
    #                 to_slug = slugify(to_slug + '-' + str(get_random_code()))
    #                 ex = Post.objects.filter(slug=to_slug).exists()
    #         else:
    #             to_slug = slugify(str(self.user) + '-' + 'post' + str(get_random_code()))
    #     self.slug = to_slug
    #     super().save(*args, **kwargs)

class PostImage(models.Model):
    '''This model handles a particular image(s) of a post and its full functionality is 
    backed by a signal - Serving web clients images that are too big probably because
    loading time will be high likely to lead into unresponsive website'''
    
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='post-images',validators=[FileExtensionValidator(['png','jpg','gif','jpeg'])])
    thumbnail = models.ImageField(upload_to='post_thumbnails',null=True, blank=True)
    
class Comment(models.Model):
    '''This class defines particulars of a comment; comment-related details such as author, 
    likes count alongside other features represnted by the fields.
    Ordering of the post listing is from the most recent post downards as defined in the meta class.'''
    
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
    '''This class represents the like object, all the related details such as the liker are defined.
    Ordering of likes follow same suit as in the comments and posts'''
    
    user = models.ForeignKey("profiles.Profile", on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    value = models.CharField(choices=LIKE_CHOICES, blank=True, max_length=8)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f"{self.user} - {self.post} - {self.value}"
