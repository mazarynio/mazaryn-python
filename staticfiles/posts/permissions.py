from rest_framework import permissions
from rest_framework.permissions import BasePermission
from rest_access_policy import AccessPolicy


class PostAccessPolicy(AccessPolicy):

    statements = [
        {
            "action": ["list", "retrieve"],
            "principal": "*",
            "effect": "allow",
            # "condition": "is_author"
        },
        # {
        #     "action": ["destroy"],
        #     "principal": "*",
        #     "effect": "allow",
        #     "condition": "is_author",
        # },
    ]

    def is_author(self, request, view, id) -> bool:
        post = view.get_object()
        return request.user == post.author


class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """
    message = "You're not allowed to edit this post"

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Instance must have an attribute named `author`.
        return obj.author == request.user
