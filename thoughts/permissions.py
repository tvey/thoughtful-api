import re

from rest_framework import permissions


class IsOwnerOrFakeOrReadOnly(permissions.BasePermission):
    """Allow to update owned items or items owned by fake (philo-) users;
    restrict delete only to owned items."""

    def has_object_permission(self, request, view, obj):
        owned_by_request_user = obj.author == request.user

        if request.method in permissions.SAFE_METHODS:
            return True
        if request.method == 'DELETE':
            return owned_by_request_user
        if request.method in ['PUT', 'PATCH']:
            owned_by_philo = re.match(r'philo\d{2}$', obj.author.username)
            return owned_by_request_user or owned_by_philo
        return False
