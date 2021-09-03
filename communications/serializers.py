from django.db.models import fields
from rest_framework import serializers
from communications.models import Room, Message

#Model Serializer
class MessageSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    
    class Meta:
        model = Message
        #Specify fields to include/serialize
        fields = [
            'id',
            'room',
            'message',
            'author', 
            'friend',
            'timestamp'
        ]

        read_only_fields = ('room', 'timestamp',)

class GetAllMessageRequestSerializer(serializers.Serializer):
    authorId = serializers.IntegerField(required=True)


class FriendtoFriendMessagesSerializer(serializers.Serializer):
    authorId = serializers.IntegerField(required=True)
    friendId = serializers.IntegerField(required=True)  


#Model Serializer
class RoomSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True)
    friend = serializers.CharField(required=False)
    
    class Meta:
        model = Room
        fields = [
            'id',
            'author',
            'friend',
            'messages'
        ]
        #generate nested representations
        depth = 1
    
    def create(self, validated_data):
        messages = validated_data.pop('messages')
        room = Room.objects.create(**validated_data)
        for message in messages:
            Message.objects.create(**message, room=room )
        
        return room