from rest_framework import serializers
from posts.models import Post, Comment


class CommentSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    post = id = serializers.IntegerField(required=False)

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
    comments = CommentSerializer(many=True)
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
        question = Post.objects.create(**validated_data)
        for comment in comments:
            Comment.objects.create(**comment, question=question)
        return question
