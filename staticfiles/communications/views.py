from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.db.models import Q
from django.http import JsonResponse

from profiles.models import Profile, Relationship
from .serializers import RoomSerializer, MessageSerializer

from rest_framework.decorators import action, api_view


def all_messages(request):
    profile = Profile.objects.get(user=request.user)
    friends = Relationship.objects.filter(
        Q(sender=profile) | Q(receiver=profile), status='accepted')
    serializer = RoomSerializer(friends, many=True)
    return JsonResponse(serializer.data, safe=False)


# Conversation with one friend
@login_required
@api_view(['POST', ])
def messages_with_one_friend(request, slug):
    if request.user.slug == slug:
        return redirect(reverse_lazy('communications:all-messages'))
    try:
        if not Profile.objects.get(slug=slug):
            return redirect(reverse_lazy('communications:all-messages'))
    except:
        return redirect(reverse_lazy('communications:all-messages'))

   # serializer = MessageSerializer(data=request.data, friend=slug)

   # if serializer.is_valid():
   #     serializer.save()

   #     data = {
   #         'status': True,
   #         'message': "Message sent"}

   # return JsonResponse(data)
