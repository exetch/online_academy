from rest_framework import permissions

from course.models import Course
from lesson.models import Lesson
from payment.models import Payment


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

class UserPaidContentPermissions(permissions.BasePermission):
    """
    Разрешает пользователям видеть и редактировать только курсы и уроки, которые они оплатили.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS or request.method in ['PUT', 'PATCH']:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        user = request.user
        if user.is_staff:
            return False

        if isinstance(obj, Course):
            return Payment.objects.filter(user=user, paid_course=obj).exists()

        if isinstance(obj, Lesson):
            return Payment.objects.filter(user=user, paid_lesson=obj).exists()

        return False