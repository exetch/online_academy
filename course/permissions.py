from rest_framework import permissions


class ModeratorOrUser(permissions.BasePermission):
    """
    Разрешение для модераторов на чтение и обновление, но не на создание или удаление.
    Пользователи, не являющиеся модераторами, могут видеть и редактировать только свои курсы и уроки.
    """

    def has_permission(self, request, view):
        if request.user.is_staff:
            if request.method in permissions.SAFE_METHODS or request.method in ['PUT', 'PATCH']:
                return True
            return False

        if request.method in ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']:
            return True

        return False

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            if request.method in permissions.SAFE_METHODS or request.method in ['PUT', 'PATCH', 'DELETE']:
                return True
            return False

        if hasattr(obj, 'owner') and request.method not in permissions.SAFE_METHODS:
            return obj.owner == request.user

        return True


