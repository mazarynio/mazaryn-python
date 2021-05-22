from .serializers import PostSerializer, CommentSerializer
from .models import Post, Comment
from .permissions import PostAccessPolicy, PostEditPermission


from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action, permission_classes
from rest_framework.response import Response


class PostViewSet(ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    lookup_field = 'id'

    # def get_permissions(self):
    #     if self.action == 'list':
    #         permission_classes = [PostEditPermission]

    # def get_object(self):
    #     queryset = self.filter_queryset(self.get_queryset())
    #     post = queryset.get(id=self.request)
    #     return super().get_object()

    @action(detail=True, methods=["GET"], permission_classes=[PostEditPermission])
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
