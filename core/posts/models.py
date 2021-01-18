from django.db import models
from django.core.validators import FileExtensionValidator
import profiles.models

# Create your models here.


class Post(models.Model):
    content = models.TextField()
    image = models.ImageField(upload_to='posts',validators=[FileExtensionValidator(['png','jpg','gif','jpeg'])], blank=True)
    liked = models.ManyToManyField("profiles.Profile", blank=True, related_name='likes')
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    author =models.ForeignKey("profiles.Profile",on_delete=models.CASCADE,related_name='posts')
    
    
    class Meta:
        ordering = ('-created',)
   
    def __str__(self):
        #return str(self.pk)
        return str( f"{self.content[:40]}..." )
    
    
    def no_of_likes(self):
        return str(self.liked.all().count())
    
    def no_of_comments(self):
        return self.comment_set.all().count()



class Comment(models.Model):
    user = models.ForeignKey("profiles.Profile", on_delete=models.CASCADE)
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    body = models.TextField(max_length=250)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(self.pk)
    
LIKE_CHOICES =(
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
    
        