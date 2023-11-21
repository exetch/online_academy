from rest_framework import generics

from course.permissions import ModeratorEditPermissions, UserPaidContentPermissions
from payment.models import Payment
from .models import Lesson
from .serializers import LessonSerializer

class LessonListCreate(generics.ListCreateAPIView):
    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Lesson.objects.all()
        else:
            paid_lessons_ids = Payment.objects.filter(user=user, paid_lesson__isnull=False).values_list('paid_lesson', flat=True)
            return Lesson.objects.filter(id__in=paid_lessons_ids)
    serializer_class = LessonSerializer
    permission_classes = [ModeratorEditPermissions, UserPaidContentPermissions]

class LessonRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Lesson.objects.all()
        else:
            paid_lessons_ids = Payment.objects.filter(user=user, paid_lesson__isnull=False).values_list('paid_lesson', flat=True)
            return Lesson.objects.filter(id__in=paid_lessons_ids)
    serializer_class = LessonSerializer
    permission_classes = [ModeratorEditPermissions, UserPaidContentPermissions]
