from rest_framework import generics

from course.permissions import ModeratorOrUser
from .models import Lesson
from .serializers import LessonSerializer

class LessonListCreate(generics.ListCreateAPIView):

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Lesson.objects.all()
        else:
            return Lesson.objects.filter(owner=user)
    serializer_class = LessonSerializer
    permission_classes = [ModeratorOrUser]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class LessonRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Lesson.objects.all()
        else:
            return Lesson.objects.filter(owner=user)
    serializer_class = LessonSerializer
    permission_classes = [ModeratorOrUser]
