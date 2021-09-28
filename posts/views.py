from .serializers import PostSerializer, CommentSerializer, PostImageSerializer
from .models import Post, Comment, PostImage
import logging
from rest_flex_fields import FlexFieldsModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import parsers


logger = logging.getLogger(__name__)


class PostViewSet(FlexFieldsModelViewSet):
    '''This class leverages on the modelviewset functionality in order to handle the required 
    posts operations ie. it returns a post, lists queryed posts etc. 
    Wholesomely, POST,GET,PUT,DELETE http requests.'''
    
    logger.info("Retrieving all posts...")

    serializer_class = PostSerializer
    queryset = Post.objects.all()
    parser_classes = parsers.MultiPartParser
    # lookup_field = 'id'

    @action(detail=True, methods=["GET"],)
    def comments(self, request, id=None):
        post = self.get_object()
        comments = Comment.objects.filter(post=post)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=200)

    @action(detail=True, methods=['POST'])
    def comment(self, request, id=None):
        post = self.get_object()
        data = request.data
        data['post'] = post.id
        serializer = CommentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)