from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.db.models import Q
from django.http import JsonResponse

from .serializers import RoomSerializer, MessageSerializer,GetAllMessageRequestSerializer,FriendtoFriendMessagesSerializer
from rest_framework.decorators import action, api_view 
from rest_framework import  generics,status
from .models import Message,Room
from rest_framework.response import Response


#This endpoint is not working yet, it might be removed later(seems redundant)
@api_view(['POST',])
def all_messages(request):
    serializer_request = GetAllMessageRequestSerializer(data = request.data)
    # profile = Profile.objects.get(user=request.user)
    # friends = Relationship.objects.filter(
    #     Q(sender=profile) | Q(receiver=profile), status='accepted')
    messages = Message.objects.filter(author_id=serializer_request['authorId']).all()
    serializer = MessageSerializer(messages, many=True)
    return JsonResponse(serializer.data, safe=False)


# Conversation with one friend
class MessageWithOneFriendView(generics.GenericAPIView):
    serializer_class= FriendtoFriendMessagesSerializer
    queryset = Message.objects.all() 
    def post(self,request):
        serializer_request = self.serializer_class(data=request.data)
        if serializer_request.is_valid():
            try:
                author = serializer_request.data['authorId']
                friend = serializer_request.data['friendId']
                room = Room.objects.get(Q(author_id=author,friend_id=friend)|Q(author_id=friend,friend_id=author)).id
                print(room)
                messages = self.queryset.filter(room_id=room).all()
                print(messages.count())
                response = MessageSerializer(messages,many=True)
                return Response(data = response.data, status=status.HTTP_200_OK)
                
            except Exception as ex:
                print(ex)
                return Response(data = str(ex), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(data = serializer_request.errors, status=status.HTTP_400_BAD_REQUEST)


class SendMessageToOneFriendView(generics.GenericAPIView):
    serializer_class = MessageSerializer
    queryset = Message.objects.all()
    def post(self,request):
        serializer_request = self.serializer_class(data=request.data)
        if serializer_request.is_valid():
            try:
                author = serializer_request.data['author']
                friend = serializer_request.data['friend']
                message = serializer_request.data['message']
                room = Room.objects.filter(Q(author_id=author,friend_id=friend)|Q(author_id=friend,friend_id=author)).count() 
                print("debug ==>{0}".format(room))
                if not room:
                    room = Room.objects.create(author_id=author,friend_id=friend)
                    print("gere")
                    room.save()
                print("=>for bug")
                room_id = Room.objects.get(Q(author_id=author,friend_id=friend)|Q(author_id=friend,friend_id=author)).id 
                
                message_obj = Message.objects.create(author_id=author,friend_id=friend,message=message,room_id=room_id)
                message_obj.save()
                return Response(data = serializer_request.data, status=status.HTTP_200_OK)
            except Exception as ex:
                print(ex)
                return Response(data = str(ex), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(data = serializer_request.errors, status=status.HTTP_400_BAD_REQUEST)