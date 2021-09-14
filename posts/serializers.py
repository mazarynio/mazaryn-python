from rest_framework import serializers
from posts.models import Post, Comment, PostImage


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
        
class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        fields = ('thumbnail')


class PostSerializer(serializers.ModelSerializer):
    '''Posts serializer 'converts'/serializes posts,serving them to and from the database.
    On http post request, create method which actually saves the data to the database 
    explicitly handles the comments - comments aren't a field in posts model.'''
    
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
            'comments'
        ]
        
        # depth = 1

    def create(self, validated_data):
        request = self.context['request']
        
        if "comments" in validated_data.keys():
            comments = validated_data.pop('comments')
        else:
            comments = list()
        post = Post.objects.create(author=request.user.profile, **validated_data)
        for comment in comments:
            Comment.objects.create(**comment, post=post)
        return post