from rest_framework.permissions import BasePermission


class IsAuthenticatedAndOwner(BasePermission):
    """
    Allows access only to authenticated users.
    """

    def has_object_permission(self, request, view, obj):
        return bool((request.user and request.user.is_authenticated) and (obj.user == request.user or request.user.is_staff))
