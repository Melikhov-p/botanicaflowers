from rest_framework.permissions import BasePermission


class IsAuthenticatedOrSuperUser(BasePermission):
    """
    Allows access only to authenticated users.
    """

    def has_permission(self, request, view):
        return bool((request.user and request.user.is_authenticated) or request.user.is_staff)
