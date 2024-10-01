from rest_framework import permissions, status
from rest_framework.response import Response
from .utilities import response_formatter


class CheckPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return Response(response_formatter(None, status.HTTP_403_FORBIDDEN, 'احراز هویت انجام نشده است!'))


def check_user_admin(user):
    if user.is_superuser and user.is_admin:
        return True
    else:
        return False
