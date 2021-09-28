from rest_framework import serializers
from posts.models import Post, Comment, PostImage
from versatileimagefield.serializers import VersatileImageFieldSerializer
from rest_flex_fields import FlexFieldsModelSerializer

class CommentSerializer(serializers.ModelSerializer):
    '''Serializes comments.'''
    
    id = serializers.IntegerField(required=False)
    
    class Meta:
        model = Comment
        fields = [
            'id',
            'post',
            'body',
            'user'
        ]
        read_only_fields = ('post',)
        
class PostImageSerializer(FlexFieldsModelSerializer):
    
    image = VersatileImageFieldSerializer(
        sizes=[
            ('full_size', 'url'),
            ('thumbnail', 'thumbnail__300x300'),
        ]
    )
    class Meta:
        model = PostImage
        fields = ('image',)


class PostSerializer(FlexFieldsModelSerializer):
    '''Posts serializer 'converts'/serializes posts,serving them to and from the database.
    On http post request, create method which actually saves the data to the database 
    explicitly handles the comments - comments aren't a field in posts model.'''
    
    image = PostImageSerializer(many=True, required=False)
    comments = CommentSerializer(many=True, required=False)
    class Meta:
        read_only_fields = ('liked','author','comments', )
        model = Post
        fields = [
            'id',
            'content',            
            'liked',
            'author',
            'created',
            'comments',
            'image',
        ]
        expandable_fields = {'image': ('posts.PostImageSerializer', {'many': True}),}

    def create(self, validated_data):
        request = self.context['request']
        r_data = self.context['request'].FILES
        
        instance = super().create(validated_data)
        
        if "comments" in validated_data.keys():
            comments = validated_data.pop('comments')
        else:
            comments = list()
        
        if "image" in validated_data.keys():
            images = validated_data.pop('image')
        else:
            pass
        
        post = Post.objects.create(**validated_data) 
        # post = Post.objects.create(author=request.user.profile, **validated_data) 
        for comment in comments:
            Comment.objects.create(**comment, post=post)
        
        post_image = PostImage.objects.create(image=r_data['image'])
        post.image.add(post_image)
        return post