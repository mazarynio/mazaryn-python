from friends.models import FriendshipRequest
from django.contrib.auth import get_user_model
# FriendshipRequest.objects.last().accept()
from django.apps import apps
User = get_user_model()

FriendshipRequest.objects.all().delete()

Friend = apps.get_model("friends", "Friend")
Friend_ship = apps.get_model("friendship", "Friend")
u1, u2 = User.objects.filter()[:2]
fs = Friend_ship.objects.add_friend(u1, u2)
fs.accept()
