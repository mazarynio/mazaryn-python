from friendship.models import (Friend as FriendBaseModel, FriendshipManager as FriendshipBaseManager, bust_cache, cache,
                               cache_key, FriendshipRequest, Follow, Block)
from friendship.signals import friendship_removed, friendship_request_accepted
from django.db import models
from django.db.models import Q

"""
    Please import models from here instead importing directly form friendship app. 
"""


class FriendshipManager(FriendshipBaseManager):

    def friends(self, user):
        """
        Return a list of all friends.
        """
        key = cache_key("friends", user.pk)
        friends = cache.get(key)

        if friends is None:
            qs = (
                Friend.objects.select_related("from_user", "to_user")
                .filter(to_user=user, is_active=True)
                .all()
            )
            friends = [u.from_user for u in qs]
            cache.set(key, friends)

        return friends

    def are_friends(self, user1, user2):
        """
        Are these two users friends?
        """
        friends1 = cache.get(cache_key("friends", user1.pk))
        friends2 = cache.get(cache_key("friends", user2.pk))
        if friends1 and user2 in friends1:
            return True
        elif friends2 and user1 in friends2:
            return True
        else:
            try:
                Friend.objects.get(to_user=user1, from_user=user2, is_active=True)
                return True
            except Friend.DoesNotExist:
                return False

    def remove_friend(self, from_user, to_user):
        """
        Destroy a friendship relationship.
        """
        try:
            qs = Friend.objects.filter(Q(to_user=to_user, from_user=from_user) | Q(to_user=from_user, from_user=to_user))
            distinct_qs = qs.distinct().all()

            if distinct_qs:
                friendship_removed.send(
                    sender=distinct_qs[0], from_user=from_user, to_user=to_user
                )
                qs.update(is_active=False)
                bust_cache("friends", to_user.pk)
                bust_cache("friends", from_user.pk)
                return True
            else:
                return False
        except Friend.DoesNotExist:
            return False


class Friend(FriendBaseModel):
    is_active = models.BooleanField(default=True)
    objects = FriendshipManager()



def accept(self):
    """
    Accept this friendship request
    """
    if Friend.objects.filter(from_user=self.from_user, to_user=self.to_user).exists():
        Friend.objects.filter(from_user=self.from_user, to_user=self.to_user).update(is_active=True)
    else:
        Friend.objects.create(from_user=self.from_user, to_user=self.to_user)
    if Friend.objects.filter(from_user=self.to_user, to_user=self.from_user).exists():
        Friend.objects.create(from_user=self.to_user, to_user=self.from_user).update(is_active=True)
    else:
        Friend.objects.create(from_user=self.to_user, to_user=self.from_user)

    friendship_request_accepted.send(
        sender=self, from_user=self.from_user, to_user=self.to_user
    )

    self.delete()

    # Delete any reverse requests
    FriendshipRequest.objects.filter(
        from_user=self.to_user, to_user=self.from_user
    ).delete()

    # Bust requests cache - request is deleted
    bust_cache("requests", self.to_user.pk)
    bust_cache("sent_requests", self.from_user.pk)
    # Bust reverse requests cache - reverse request might be deleted
    bust_cache("requests", self.from_user.pk)
    bust_cache("sent_requests", self.to_user.pk)
    # Bust friends cache - new friends added
    bust_cache("friends", self.to_user.pk)
    bust_cache("friends", self.from_user.pk)
    return True

FriendshipRequest.accept = accept

