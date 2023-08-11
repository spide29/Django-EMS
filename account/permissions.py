from rest_framework.permissions import BasePermission

class IsNotSuperuser(BasePermission):
    """
    Custom permission to allow only non-superusers.
    """
    def has_permission(self, request, view):
        return not request.user.is_superuser
