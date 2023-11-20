from rest_framework import permissions

class ModeratorEditPermissions(permissions.BasePermission):
    """
    Разрешение для модераторов на чтение и обновление, но не на создание или удаление.
    """

    def has_permission(self, request, view):
        if request.user.is_staff:
            if request.method in permissions.SAFE_METHODS or request.method in ['PUT', 'PATCH']:
                return True
            return False
        return True

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            if request.method in permissions.SAFE_METHODS or request.method in ['PUT', 'PATCH']:
                return True
            return False
        return True
