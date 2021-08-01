from rest_framework import serializers
from posts.models import Post, Comment


class CommentSerializer(serializers.ModelSerializer):
    '''Posts serializer 'converts'/serializes comments,serving them to and from the database.'''
    
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


class PostSerializer(serializers.ModelSerializer):
    '''Posts serializer 'converts'/serializes posts,serving them to and from the database.
    On http post request, create method which actually saves the data to the database 
    explicitly handles the comments - comments aren't a field in posts model.'''
    
    comments = CommentSerializer(many=True, required=False)
    image = serializers.ImageField(required=False)

    class Meta:
        model = Post
        fields = [
            'id',
            'image',
            'content',
            'liked',
            'created',
            'author',
            'comments'
        ]
        depth = 1

    def create(self, validated_data):
        comments = validated_data.pop('comments')
        post = Post.objects.create(**validated_data)
        for comment in comments:
            Comment.objects.create(**comment, post=post)
        return post
